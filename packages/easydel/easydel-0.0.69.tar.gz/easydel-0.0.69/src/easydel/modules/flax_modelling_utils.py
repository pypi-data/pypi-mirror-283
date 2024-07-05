import functools
import math
from functools import partial
from typing import List, Literal, Optional, Sequence

import chex
import einops
import fjformer
import jax
from einops import rearrange
from fjformer.bit_quantization import config as q_config
from fjformer.bit_quantization import q_flax
from flax import linen as nn
from flax.linen import combine_masks
from jax import lax
from jax import numpy as jnp
from jax.experimental.mesh_utils import create_device_mesh
from jax.experimental.shard_map import shard_map
from jax.interpreters import pxla
from jax.sharding import PartitionSpec

from easydel.etils.errors import EasyDeLBlockWiseFFNError
from easydel.etils.partition_module import PartitionAxis
from easydel.modules.easydel_modelling_utils import EasyMethod

ACT2FN = {
    "gelu": partial(nn.gelu, approximate=False),
    "relu": nn.relu,
    "silu": nn.swish,
    "swish": nn.swish,
    "gelu_new": partial(nn.gelu, approximate=True),
    "gelu_pytorch_tanh": partial(nn.gelu, approximate=True),
    "tanh": nn.tanh,
    "sigmoid": nn.sigmoid,
    "leaky_relu": partial(nn.leaky_relu, negative_slope=0.01),
    "glu": nn.glu,
    "elu": nn.elu,
    "softmax": nn.softmax,
}


def canonicalize_dtype(
    *args, dtype: Optional[chex.ArrayDType] = None, inexact: bool = True
) -> chex.ArrayDType:
    """Canonicalize an optional dtype to the definitive dtype.

    If the ``dtype`` is None this function will infer the dtype. If it is not
    None it will be returned unmodified or an exceptions is raised if the dtype
    is invalid.
    from the input arguments using ``jnp.result_type``.

    Args:
      *args: JAX array compatible values. None values
        are ignored.
      dtype: Optional dtype override. If specified the arguments are cast to
        the specified dtype instead and dtype inference is disabled.
      inexact: When True, the output dtype must be a subdtype
      of `jnp.inexact`. Inexact dtypes are real or complex floating points. This
      is useful when you want to apply operations that don't work directly on
      integers like taking a mean for example.
    Returns:
      The dtype that *args should be cast to.
    """
    if dtype is None:
        args_filtered = [jax.numpy.asarray(x) for x in args if x is not None]
        dtype = jax.numpy.result_type(*args_filtered)
        if inexact and not jax.numpy.issubdtype(dtype, jax.numpy.inexact):
            dtype = jax.numpy.promote_types(jax.numpy.float32, dtype)
    if inexact and not jax.numpy.issubdtype(dtype, jax.numpy.inexact):
        raise ValueError(f"Dtype must be inexact: {dtype}")
    return dtype


def get_names_from_partition_spec(partition_specs):
    """The get_names_from_partition_spec function takes a partition_specs argument, which is either a dictionary or list.
    If it's a dictionary, the function converts it to a list of values. Then for each item in the partition_specs list:
        If the item is None, continue (do nothing) and move on to next iteration of loop.
        If the item is an instance of str (i.e., if it's just one string), add that string to names set and move
        on to next iteration of loop.
        Otherwise, (if not None or str), call get_names_from_partition_spec recurs

    Args:
        partition_specs: Define the partitioning of a table

    Returns:
        A list of the names of all partitions
    """
    names = set()
    if isinstance(partition_specs, dict):
        partition_specs = partition_specs.values()
    for item in partition_specs:
        if item is None:
            continue
        elif isinstance(item, str):
            names.add(item)
        else:
            names.update(get_names_from_partition_spec(item))

    return list(names)


def names_in_mesh(*names):
    """The names_in_mesh function is a decorator that can be used to check whether
    the names of the axes passed into a function are valid.  It will raise an
    exception if any of the axis names are not in the physical mesh.  For example,
    if you have a function that takes two axes as arguments, and you want to make sure they're both in your mesh:

    Args:
        *names: Collect all the names passed to the function into a
            tuple

    Returns:
        A boolean indicating whether all the given
    """
    return set(names) <= set(pxla.thread_resources.env.physical_mesh.axis_names)


with_sharding_constraint = fjformer.with_sharding_constraint


def get_gradient_checkpoint_policy(name):
    """
    The get_gradient_checkpoint_policy function is a helper function that returns the gradient checkpoint policy
        specified by the name parameter.

    :param name: Select the checkpoint policy from the dictionary
    :return: A function that is used in the jax

    """
    gradients = dict(
        everything_saveable=jax.checkpoint_policies.everything_saveable,
        nothing_saveable=jax.checkpoint_policies.nothing_saveable,
        dots_saveable=jax.checkpoint_policies.dots_saveable,
        checkpoint_dots=jax.checkpoint_policies.checkpoint_dots,
        dots_with_no_batch_dims_saveable=jax.checkpoint_policies.dots_with_no_batch_dims_saveable,
        checkpoint_dots_with_no_batch_dims=jax.checkpoint_policies.checkpoint_dots_with_no_batch_dims,
        save_anything_except_these_names=jax.checkpoint_policies.save_anything_except_these_names,
        save_any_names_but_these=jax.checkpoint_policies.save_any_names_but_these,
        save_only_these_names=jax.checkpoint_policies.save_only_these_names,
        save_from_both_policies=jax.checkpoint_policies.save_from_both_policies,
    )
    return gradients[name]


def precompute_freq_cis(
    dim,
    max_position_embeddings=2048,
    base=10000,
    scaling_factor=1.0,
    rope_type: Optional[
        Literal[
            "none",
            "linear",
            "dynamic",
            "yarn",
            "su",
        ]
    ] = None,
    t_dtype: jnp.dtype = jnp.int32,
    original_max_position_embeddings: Optional[int] = None,
    long_factor: Optional[List[float]] = None,
    short_factor: Optional[List[float]] = None,
):
    def _calc_yarn_scaling_factor(scale):
        if scale <= 1.0:
            return 1.0
        return math.sqrt(
            1 + math.log(scale) / math.log(original_max_position_embeddings)
        )

    def _calc_su_scaling_factor(scale):
        if scale <= 1.0:
            return 1.0
        return math.sqrt(
            1 + math.log(scale) / math.log(original_max_position_embeddings)
        )

    if t_dtype == jnp.int64:
        jax.config.update("jax_enable_x64", True)

    if rope_type is None or rope_type == "none":
        t = jax.numpy.arange(max_position_embeddings, dtype=t_dtype)
        inv_freq = 1.0 / (
            base ** (jax.numpy.arange(0, dim, 2, dtype=jax.numpy.float32) / dim)
        )
        freq = jax.numpy.einsum("i , j -> i j", t, inv_freq).astype("float32")
        embed = jax.numpy.concatenate((freq, freq), axis=-1)
        return jax.numpy.sin(embed)[:, :], jax.numpy.cos(embed)[:, :]
    elif rope_type == "linear":
        t = jax.numpy.arange(max_position_embeddings, dtype=t_dtype)
        t = t / scaling_factor
        inv_freq = 1.0 / (
            base ** (jax.numpy.arange(0, dim, 2, dtype=jax.numpy.float32) / dim)
        )
        freq = jax.numpy.einsum("i , j -> i j", t, inv_freq).astype("float32")

        embed = jax.numpy.concatenate((freq, freq), axis=-1)
        return jax.numpy.sin(embed)[:, :], jax.numpy.cos(embed)[:, :]
    elif rope_type == "dynamic":
        t = jax.numpy.arange(max_position_embeddings, dtype=t_dtype)
        base = base * (scaling_factor - (scaling_factor - 1)) ** (dim / (dim - 2))
        inv_freq = 1.0 / (
            base ** (jax.numpy.arange(0, dim, 2, dtype=jax.numpy.float32) / dim)
        )
        freq = jax.numpy.einsum("i , j -> i j", t, inv_freq).astype("float32")

        embed = jax.numpy.concatenate((freq, freq), axis=-1)
        return jax.numpy.sin(embed)[:, :], jax.numpy.cos(embed)[:, :]
    elif rope_type == "su":
        assert (
            original_max_position_embeddings is not None
        ), "No original max position embeddings is provided"
        if max_position_embeddings > original_max_position_embeddings:
            ext_factors = jnp.array(long_factor, dtype=jnp.float32)
        else:
            ext_factors = jnp.array(short_factor, dtype=jnp.float32)

        inv_freq = (
            1.0
            / (
                ext_factors
                * base
                ** (jnp.arange(0, dim, 2, dtype=t_dtype).astype(jnp.float32) / dim)
            )[None, :, None]
        )
        position_ids = (
            jnp.arange(0, max_position_embeddings, dtype="i4")
            .reshape(1, -1)[:, None, :]
            .astype("float32")
        )
        freqs = (inv_freq @ position_ids).transpose(0, 2, 1)
        scaling_factor = _calc_su_scaling_factor(
            max_position_embeddings / original_max_position_embeddings
        )
        emb = jnp.concatenate((freqs, freqs), axis=-1)
        cos = jnp.cos(emb) * scaling_factor
        sin = jnp.sin(emb) * scaling_factor
        return sin[0], cos[0]
    elif rope_type == "yarn":
        assert (
            original_max_position_embeddings is not None
        ), "No original max position embeddings is provided"
        if max_position_embeddings > original_max_position_embeddings:
            ext_factors = jnp.array(long_factor, dtype=jnp.float32)
        else:
            ext_factors = jnp.array(short_factor, dtype=jnp.float32)

        inv_freq = (
            1.0
            / (
                ext_factors
                * base
                ** (jnp.arange(0, dim, 2, dtype=t_dtype).astype(jnp.float32) / dim)
            )[None, :, None]
        )
        position_ids = (
            jnp.arange(0, max_position_embeddings, dtype="i4")
            .reshape(1, -1)[:, None, :]
            .astype("float32")
        )
        freqs = (inv_freq @ position_ids).transpose(0, 2, 1)
        scaling_factor = _calc_yarn_scaling_factor(
            max_position_embeddings / original_max_position_embeddings
        )
        emb = jnp.concatenate((freqs, freqs), axis=-1)
        cos = jnp.cos(emb) * scaling_factor
        sin = jnp.sin(emb) * scaling_factor
        return sin[0], cos[0]
    else:
        raise "wrong rope type has been given"


def rotate_half(x):
    """The rotate_half function takes a complex-valued array and rotates the
    phase of its second half by 180 degrees. This is equivalent to multiplying
    the second half by -i, or equivalently rotating it 90 degrees counterclockwise.

    Args:
        x: Specify the input array

    Returns:
        A new array that is the same as the input
    """
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return jax.numpy.concatenate((-x2, x1), axis=-1)


def apply_rotary_pos_emb(tensor, sin_, cos_):
    """The apply_rotary_pos_emb function applies a rotary positional embedding to the input tensor.
    b,h,s,d or pytorch style

    Args:
        tensor: Store the tensor that is passed into the function
        sin_: Rotate the tensor by pi/2
        cos_: Apply the cosine function to the tensor

    Returns:
        A tensor with the same shape as the input tensor
    """
    b, h, s, d = tensor.shape
    return (tensor * cos_[:, :, :s, :]) + (rotate_half(tensor) * sin_[:, :, :s, :])


def get_ranks_and_size(mesh):
    """The get_ranks_and_size function is used to determine the number of MPI processes
    (``mp_node_size``) and the number of devices per process (``dp_node_size``).
    The ``mesh.shape[mp]`` determines how many MPI processes are needed,
    and then we divide that by the local device count to get ``mp_node_size = max( 1, mp / jax.local )`.
    This means that if there are more than enough devices for all MPI ranks on a node, each rank will only use one device; otherwise it will use

    Args:
        mesh: Get the shape of the mesh

    Returns:
        A dictionary with the following keys:
    """
    out = dict(mesh=mesh)
    total_process_size = mesh.shape["tp"] * mesh.shape["sp"]
    mp_node_size = max(1, total_process_size // jax.local_device_count())
    dp_node_size = jax.process_count() // mp_node_size
    out.update(mp_node_size=mp_node_size, dp_node_size=dp_node_size)

    dp_node_rank = jax.process_index() // mp_node_size
    mp_node_rank = jax.process_index() % mp_node_size
    out.update(dp_node_rank=dp_node_rank, mp_node_rank=mp_node_rank)
    return out


def create_mesh(
    axis_dims: Sequence[int] = (1, -1, 1, 1),
    axis_names: Sequence[str] = ("dp", "fsdp", "tp", "sp"),
    backend="",
):
    """The create_mesh function creates a mesh object that can be used to shard arrays.

    Args:
        axis_dims: Sequence[int]: Specify the dimensions of the mesh
        axis_names: Sequence[str]: Name the axes of the mesh
        backend: Specify the backend to use

    Returns:
        A mesh object
    """
    array_devices = jax.numpy.ones(
        (len(jax.devices() if backend == "" else jax.devices(backend)), 1)
    )
    resh = array_devices.reshape(axis_dims).shape

    return jax.sharding.Mesh(create_device_mesh(resh), axis_names)


def add_start_docstrings(*docstr):
    """The add_start_docstrings function is a decorator that adds the docstrings to the beginning of a function.
    The add_start_docstrings function takes in an arbitrary number of strings and returns a decorator.
    The returned decorator takes in one argument, fn, which is assumed to be a function. The docstring for fn is set equal to
    the concatenation of all the strings passed into add_start_docstrings plus (if it exists) the original docstring for fn.

    Args:
        *docstr: Pass in a variable number of arguments to the function

    Returns:
        A decorator that adds the docstrings to the function
    """

    def docstring_decorator(fn):
        fn.__doc__ = "".join(docstr) + (fn.__doc__ if fn.__doc__ is not None else "")
        return fn

    return docstring_decorator


def get_dot_general_by_bits(
    bits: Optional[int] = None,
    mode: Literal["train", "serve", "convert"] = EasyMethod.TRAIN,
) -> dict:
    """The get_general_dot function is a helper function that returns a q_flax.QDotGeneral object
    with the specified number of bits for forward and backward passes. If no bits are specified,
    the function returns None.

    Args:
        bits: Optional[int]: Specify the number of bits for quantization
        mode: EasyMethod: Specify the use of model to init the QDot
            Method for (e.q TRAIN,SERVE,...)

    Returns:
        A dict that contain dot_general_cls
    """
    if mode == EasyMethod.TRAIN:
        rhs_quant_mode = q_flax.QuantMode.TRAIN
    elif mode == EasyMethod.EVAL or mode == EasyMethod.SERVE:
        rhs_quant_mode = q_flax.QuantMode.SERVE
    elif mode == EasyMethod.CONVERT:
        rhs_quant_mode = q_flax.QuantMode.CONVERT
    else:
        raise ValueError("Unknown Quant Method for EasyMethod")
    if bits is not None:
        return {
            "dot_general_cls": functools.partial(
                q_flax.QDotGeneral,
                q_config.fully_quantized(fwd_bits=bits, bwd_bits=bits),
                rhs_quant_mode=rhs_quant_mode,
            )
        }
    return {}  # empty just in case of not getting any error


class BaseJAXAttentionModule(nn.Module):
    config: "EasyDeLPretrainedConfig"  # type: ignore  # noqa

    @staticmethod
    def _transpose_sequence_head(query, key, value):
        """The _transpose_sequence_head function transposes the query, key and value matrices.

        Args:
            query: Get the attention weights for each of the heads
            key: Determine the number of heads
            value: Store the values of the input

        Returns:
            The transpose of the query, key and value matrices
        """
        return (
            jnp.transpose(query, (0, 2, 1, 3)),
            jnp.transpose(key, (0, 2, 1, 3)),
            jnp.transpose(value, (0, 2, 1, 3)),
        )

    @nn.compact
    def _concatenate_to_cache(self, key, value, query_states, attention_mask):
        """The _concatenate_to_cache function is used to concatenate the key and value vectors
        of a query_states with those of previous queries. This allows for the attention mechanism to
        look at all previous queries when computing its output. The function takes in three
        arguments: key, value, and query_states. It also uses two variables that are stored in the cache:
        cached_key and cached_value.

        Args:
            self: Access the variables stored in the cache
            key: Store the keys of the encoder-decoder attention
            value: Initialize the cached_value variable
            query_states: Determine the number of cache vectors to
                update
            attention_mask: Mask out the padded vectors in the cache

        Returns:
            The key, value and attention_mask
        """
        do_quantize_kv_cache = self.config.quantize_kv_cache
        is_initialized = self.has_variable("cache", "cached_key")
        if do_quantize_kv_cache:
            cached_key = self.variable(
                "cache", "cached_key", jnp.zeros, key.shape, jnp.uint8
            )
            cached_value = self.variable(
                "cache", "cached_value", jnp.zeros, value.shape, jnp.uint8
            )
            cached_key_scale = self.variable(
                "cache",
                "cached_key_scale",
                jnp.zeros,
                key.shape[0:-1] + (1,),
                key.dtype,
            )
            cached_value_scale = self.variable(
                "cache",
                "cached_value_scale",
                jnp.zeros,
                value.shape[0:-1] + (1,),
                value.dtype,
            )
            cached_key_minval = self.variable(
                "cache",
                "cached_key_minval",
                jnp.zeros,
                key.shape[0:-1] + (1,),
                key.dtype,
            )
            cached_value_minval = self.variable(
                "cache",
                "cached_value_minval",
                jnp.zeros,
                value.shape[0:-1] + (1,),
                value.dtype,
            )
            cache_index = self.variable(
                "cache", "cache_index", lambda: jnp.array(0, dtype=jnp.int32)
            )
        else:
            cached_key_scale = None
            cached_value_scale = None
            cached_value_minval = None
            cached_key_minval = None
            cached_key = self.variable(
                "cache", "cached_key", jnp.zeros, key.shape, key.dtype
            )
            cached_value = self.variable(
                "cache", "cached_value", jnp.zeros, value.shape, value.dtype
            )
            cache_index = self.variable(
                "cache", "cache_index", lambda: jnp.array(0, dtype=jnp.int32)
            )
        paxs: PartitionAxis = self.config.partition_axis
        if is_initialized:
            *batch_dims, max_length, num_heads, depth_per_head = cached_key.value.shape
            cur_index = cache_index.value
            if query_states.shape[1] == 1 and self.config.use_sharded_kv_caching:
                mesh = self.config.get_mesh()

                def fn(_cached_key, _cached_value, _key, _value, _cur_index):
                    assert _key.shape[1] == 1 and _value.shape[1] == 1, (
                        _key.shape,
                        _value.shape,
                    )
                    sp_size = max_length // mesh.shape["sp"]
                    axis_index = jax.lax.axis_index("sp")
                    _cur_index = _cur_index - axis_index * sp_size
                    _key, _value = jax.lax.cond(
                        jnp.logical_and(_cur_index >= 0, _cur_index < sp_size),
                        lambda: (
                            _cached_key.at[:, _cur_index].set(_key[:, -1]),
                            _cached_value.at[:, _cur_index].set(_value[:, -1]),
                        ),
                        lambda: (_cached_key, _cached_value),
                    )
                    return _key, _value

                fn = shard_map(
                    fn,
                    mesh=mesh,
                    in_specs=(
                        PartitionSpec(
                            paxs.batch_axis,
                            paxs.key_sequence_axis,
                            paxs.head_axis,
                            paxs.attention_dim_axis,
                        ),
                        PartitionSpec(
                            paxs.batch_axis,
                            paxs.key_sequence_axis,
                            paxs.head_axis,
                            paxs.attention_dim_axis,
                        ),
                        PartitionSpec(
                            paxs.batch_axis,
                            None,
                            paxs.head_axis,
                            paxs.attention_dim_axis,
                        ),
                        PartitionSpec(
                            paxs.batch_axis,
                            None,
                            paxs.head_axis,
                            paxs.attention_dim_axis,
                        ),
                        PartitionSpec(),
                    ),
                    out_specs=(
                        PartitionSpec(
                            paxs.batch_axis,
                            paxs.key_sequence_axis,
                            paxs.head_axis,
                            paxs.attention_dim_axis,
                        ),
                        PartitionSpec(
                            paxs.batch_axis,
                            paxs.key_sequence_axis,
                            paxs.head_axis,
                            paxs.attention_dim_axis,
                        ),
                    ),
                    check_rep=False,
                )
                key, value = fn(
                    cached_key.value, cached_value.value, key, value, cur_index
                )
            else:
                *batch_dims, max_length, num_heads, depth_per_head = (
                    cached_key.value.shape
                )
                cur_index = cache_index.value
                indices = (0,) * len(batch_dims) + (cur_index, 0, 0)  # type:ignore
                if do_quantize_kv_cache:
                    key_val = dequantize_kv_cache(
                        cached_key.value,
                        cached_key_scale.value,
                        cached_key_minval.value,
                        key.dtype,
                    )
                    value_val = dequantize_kv_cache(
                        cached_value.value,
                        cached_value_scale.value,
                        cached_key_minval.value,
                        value.dtype,
                    )
                else:
                    key_val = cached_key.value
                    value_val = cached_value.value

                key = lax.dynamic_update_slice(key_val, key, indices)
                value = lax.dynamic_update_slice(value_val, value, indices)
                num_updated_cache_vectors = query_states.shape[1]
                pad_mask = jnp.broadcast_to(
                    jnp.arange(max_length) < cur_index + num_updated_cache_vectors,
                    tuple(batch_dims) + (1, num_updated_cache_vectors, max_length),
                )
                attention_mask = combine_masks(pad_mask, attention_mask)
            if do_quantize_kv_cache:
                kq, ks, km = quantize_kv_cache(key)
                vq, vs, vm = quantize_kv_cache(value)

                cached_key.value = kq
                cached_key_scale.value = ks.astype(self.dtype)
                cached_key_minval.value = km.astype(self.dtype)

                cached_value.value = vq
                cached_value_scale.value = vs.astype(self.dtype)
                cached_value_minval.value = vm.astype(self.dtype)
            else:
                cached_key.value = key
                cached_value.value = value

            num_updated_cache_vectors = query_states.shape[1]
            cache_index.value = cache_index.value + num_updated_cache_vectors
        return key, value, attention_mask

    @staticmethod
    def repeat_key_value(key, value, num_reps: int):
        key = einops.repeat(
            key,
            "b s h d -> b s (h r) d",
            r=num_reps,
        )
        value = einops.repeat(
            value,
            "b s h d -> b s (h r) d",
            r=num_reps,
        )
        return key, value


def block_wise_ffn(remat_ffn, inputs, chunk_size: int, deterministic: bool):
    generating = inputs.shape[1] == 1
    try:
        if generating:
            return remat_ffn(inputs, deterministic)
        else:
            inputs = rearrange(inputs, "b (c n) d -> b c n d", c=chunk_size)

            def scan_ffn(remat_ffn_, carry, hidden_states):
                outputs = remat_ffn_(hidden_states, deterministic)
                return carry, outputs

            scan_axis = inputs.ndim - 2
            _, output = nn.scan(
                scan_ffn,
                variable_broadcast="params",
                split_rngs={"params": False, "dropout": True},
                in_axes=scan_axis,
                out_axes=scan_axis,
            )(remat_ffn, None, inputs)
            output = rearrange(output, "b c n d -> b (c n) d")
            return output
    except Exception as e:
        raise EasyDeLBlockWiseFFNError(
            "You Are using BlockWise FFN from near-infinite-context length paper and you might be passing "
            "input arguments in wrong way in case that you don't want to use this just pass `use_scan_mlp=False` in "
            "model config or in config_kwargs in AutoEasyDeLModelForCausalLM or change `scan_mlp_chunk_size` "
            f"in configs for more information read Docs.\nOriginal Error\n{e}"
        )


def read_depth(params: dict, path: str | None = None, state: dict | None = None):
    if state is None:
        state = {}
    for key, value in params.items():
        if isinstance(value, dict):
            accureated_path = path + "/" + key if path is not None else key
            state = read_depth(
                params[key], path=key if path is None else accureated_path, state=state
            )
        else:
            value_string = type(value).__name__ + f"(shape={value.shape})"
            state[path] = value_string
    return state


def get_maximum_depths(dictionary: dict):
    maximums = {}
    minimums = {}
    for k, v in dictionary.items():
        splits = k.split("/")
        for index, split in enumerate(splits):
            try:
                split = int(split)
                if str(index) in maximums.keys():
                    current = maximums[str(index)]
                    if current < split:
                        maximums[str(index)] = split
                else:
                    maximums[str(index)] = split
                if str(index) in minimums.keys():
                    split = int(split)
                    if str(index) in minimums.keys():
                        current = minimums[str(index)]
                        if current > split:
                            minimums[str(index)] = split
                else:
                    minimums[str(index)] = split
            except ValueError:
                ...
    return maximums, minimums


def control_mlp_sharding(x: jax.Array, partition_axis: PartitionAxis):
    """
    this functions is disabled for now, it will cause breakdown and incorrect computation on gpu with CU lower than 7.5
    """
    # batch_size, sequence_length, hidden_size = x.shape
    # is_gen = sequence_length == 1
    # mesh = jax.interpreters.pxla.thread_resources.env.physical_mesh
    # if not mesh.empty:
    #     partition_spec = PartitionSpec(
    #         partition_axis.batch_axis,
    #         None if is_gen else partition_axis.sequence_axis,
    #         (
    #             partition_axis.hidden_state_axis
    #             if (
    #                     mesh.shape[partition_axis.hidden_state_axis] / hidden_size
    #             ).is_integer()
    #             else None
    #         ),
    #     )
    #     x = with_sharding_constraint(x, partition_spec)
    return x


@partial(jax.jit, static_argnames=["reformat"])
def quantize_kv_cache(fdata, reformat: bool = True):
    """Quantizes the given tensor using scalar quantization.

    Args:
        fdata: The input JAX array to quantize.

    Returns:
        A tuple containing:
            - The quantized JAX array.
            - The scale factor used for quantization.
            - The zero-point offset used for quantization.
    """
    if reformat:
        fdata = fdata.transpose(0, 2, 1, 3)
    qmin = jnp.array(jnp.iinfo(jnp.uint8).min)
    qmax = jnp.array(jnp.iinfo(jnp.uint8).max)
    shape = fdata.shape

    fdata_cal = jnp.reshape(fdata, fdata.shape[:2] + (-1,))
    fmax = jnp.max(fdata_cal, axis=-1, keepdims=True)
    fmin = jnp.min(fdata_cal, axis=-1, keepdims=True)

    # Ensure qmax and qmin are on the same device as fdata
    qmax = jax.tree_map(lambda x: jnp.array(x, dtype=fdata.dtype), qmax)
    qmin = jax.tree_map(lambda x: jnp.array(x, dtype=fdata.dtype), qmin)

    scale = (fmax - fmin) / (qmax - qmin)

    zero = qmin - fmin / scale

    # Expand dimensions of scale and zero to match fdata
    scale = jnp.expand_dims(scale, axis=-1).repeat(shape[2], axis=-2)
    zero = jnp.expand_dims(zero, axis=-1).repeat(shape[2], axis=-2)
    # Quantize
    res_data = fdata / scale + zero
    qdata = jnp.clip(res_data, qmin, qmax).astype(jnp.uint8)
    if reformat:
        qdata, scale, zero = map(
            lambda x: x.transpose(0, 2, 1, 3), [qdata, scale, zero]
        )
        # print(f"{qdata.shape=}, {scale.shape=}, {zero.shape=}")
    return qdata, scale, zero


@partial(jax.jit, static_argnames=["float_dtype", "reformat"])
def dequantize_kv_cache(
    array_quant: jax.Array,
    scale: jax.Array,
    zero: jax.Array,
    float_dtype: jnp.dtype = jnp.float16,
    reformat: bool = True,
):
    """
    The function `dequantize` takes a quantized array, scale, minimum values, and float data
    type, and returns the dequantized array.

    Args:
      array_quant (Array): The `array_quant` parameter is an array containing quantized
    values that need to be dequantized.
      scale (Array): The `scale` parameter is an array that contains the scaling factors
    used for dequantization. It is used to scale the quantized values back to their original
    range during the dequantization process.
      zero (Array): The `zero` parameter in the `dequantize` function represents the
    minimum values used during quantization. These values are added back during
    dequantization to recover the original range of the data.
      float_dtype (jnp.dtype): The `float_dtype` parameter in the `dequantize` function is
    the data type to which the dequantized array will be converted before returning. In this
    case, the default data type is `jnp.float16`, which is a 16-bit floating-point data type
    in JAX.

    Returns:
      The `dequantize` function is returning the dequantized array. The dequantization
    process involves multiplying the quantized array (`array_quant`) by the scale factor,
    adding the minimum values, and then converting the result to the specified
    floating-point data type (`float_dtype`).
    """
    if reformat:
        array_quant, scale, zero = map(
            lambda x: x.transpose(0, 2, 1, 3), [array_quant, scale, zero]
        )
    uq = lax.convert_element_type(scale * (array_quant - zero), float_dtype)
    if reformat:
        uq = uq.transpose(0, 2, 1, 3)
    return uq
