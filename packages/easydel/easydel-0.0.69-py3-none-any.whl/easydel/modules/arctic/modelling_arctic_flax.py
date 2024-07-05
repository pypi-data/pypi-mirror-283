import functools
import math
from typing import Optional, Tuple, Union

import chex
import fjformer
import flax
import jax
from fjformer.functions import auxiliary_load_balancing_loss_func
from fjformer.linen import Dense
from flax import linen as nn
from flax.core import FrozenDict, freeze, unfreeze
from flax.linen import combine_masks
from flax.linen import partitioning as nn_partitioning
from flax.traverse_util import flatten_dict, unflatten_dict
from jax import lax
from jax import numpy as jnp
from jax.sharding import PartitionSpec
from transformers.modeling_flax_outputs import FlaxMaskedLMOutput

from easydel.modules.attention_module import AttentionModule
from easydel.modules.easydel_modelling_utils import EasyDeLFlaxPretrainedModel
from easydel.modules.flax_modelling_utils import (
    ACT2FN,
    BaseJAXAttentionModule,
    apply_rotary_pos_emb,
    block_wise_ffn,
    control_mlp_sharding,
    get_dot_general_by_bits,
    get_gradient_checkpoint_policy,
    precompute_freq_cis,
    with_sharding_constraint,
)
from easydel.modules.arctic.arctic_configuration import ArcticConfig

re_mat = nn_partitioning.remat


@flax.struct.dataclass
class MoeModelOutput:
    last_hidden_state: chex.Array = None
    hidden_states: Optional[Tuple[chex.Array]] = None
    attentions: Optional[Tuple[chex.Array]] = None
    all_router_losses: Optional[Tuple[chex.Array]] = None


@flax.struct.dataclass
class MoeCausalLMOutput(FlaxMaskedLMOutput):
    aux_loss: Optional[chex.Array] = None
    all_router_losses: Optional[Tuple[chex.Array]] = None


class ArcticRMSNorm(nn.Module):
    dim: int
    eps: float = 1e-6
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16

    def setup(self) -> None:
        self.weight = self.param(
            'kernel',
            nn.initializers.ones,
            (self.dim,),
            self.param_dtype,
        )

    def _norm(self, x: jnp.ndarray) -> jnp.ndarray:
        return x * jax.lax.rsqrt(jnp.square(x).mean(-1, keepdims=True) + self.eps)

    def __call__(self, x: jnp.ndarray) -> jnp.ndarray:
        x = x.astype(jnp.promote_types(self.dtype, jnp.float32))
        output = self._norm(x).astype(self.dtype)
        weight = fjformer.linen.control_quantization(self.weight, self.dtype)
        return output * weight


class FlaxArcticRotaryEmbedding(nn.Module):
    dtype: jnp.dtype = jnp.float32

    def __call__(self, key, query, freq_cis, position_ids):
        sin, cos = freq_cis

        sin = sin[position_ids][:, None, :, :]
        cos = cos[position_ids][:, None, :, :]

        key = apply_rotary_pos_emb(key, sin, cos)
        query = apply_rotary_pos_emb(query, sin, cos)

        return query.astype(self.dtype), key.astype(self.dtype)


class FlaxArcticAttention(BaseJAXAttentionModule):
    config: ArcticConfig
    layer_index: int
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[Union[str, jax.lax.Precision]] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        config = self.config
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = self.hidden_size // self.num_heads
        self.num_key_value_heads = config.num_key_value_heads
        self.num_key_value_groups = self.num_heads // self.num_key_value_heads
        self.max_position_embeddings = config.max_position_embeddings

        dense = functools.partial(
            Dense,
            use_bias=getattr(self.config, "attention_bias", False),
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision,
            kernel_init=nn.initializers.normal(),
            **get_dot_general_by_bits(self.config.bits, self.config.easy_method)
        )

        self.q_proj = dense(self.num_heads * self.head_dim)
        self.k_proj = dense(self.num_key_value_heads * self.head_dim)
        self.v_proj = dense(self.num_key_value_heads * self.head_dim)
        self.o_proj = dense(self.num_key_value_heads * self.head_dim)
        self.rotary = FlaxArcticRotaryEmbedding(self.dtype)
        self.attention_performer = AttentionModule(
            use_sharding_constraint=self.config.use_sharding_constraint,
            block_k_major=self.config.block_k_major,
            block_b=self.config.block_b,
            block_q=self.config.block_q,
            block_k=self.config.block_k,
            block_q_major_dkv=self.config.block_q_major_dkv,
            block_k_major_dkv=self.config.block_k_major_dkv,
            block_k_major_dq=self.config.block_k_major_dq,
            block_k_dkv=self.config.block_k_dkv,
            block_q_dkv=self.config.block_q_dkv,
            block_q_dq=self.config.block_q_dq,
            block_k_dq=self.config.block_k_dq,
            num_attention_heads=self.config.num_attention_heads,
            attention_dropout=self.config.attention_dropout,
            head_dims=self.head_dim,
            shard_attention_computation=self.config.shard_attention_computation,
            precision=self.precision,
            force_float32_tpu=True,
            attn_mechanism=self.config.attn_mechanism,
            dtype=self.config.attn_dtype,
            partition_axis=self.config.partition_axis,
            scan_ring_attention=self.config.scan_ring_attention,
            mesh=self.config.get_mesh(),
            sm_scale=1 / math.sqrt(self.head_dim),
            axis_name=self.config.attention_axis_name,
            backward_pass_impl=self.config.flash_attention_backward_pass_impl
        )

    def apply_rotary(self, batch_size, sequence_length, query, key, value, freq_cis, position_ids):

        query, key, value = self._transpose_sequence_head(query, key, value)
        query, key = self.rotary(
            position_ids=position_ids, query=query, key=key, freq_cis=freq_cis)
        return self._transpose_sequence_head(query, key, value)

    def _merge_heads(self, hidden_states):
        return hidden_states.reshape(hidden_states.shape[:2] + (self.hidden_size,))

    def __call__(
            self,
            hidden_states: chex.Array,
            freq_cis: Tuple[chex.Array, chex.Array],
            attention_mask: chex.Array,
            causal_mask: chex.Array,
            position_ids: chex.Array,
            segment_ids: Optional[chex.Array] = None,
            deterministic: bool = True,
            init_cache: bool = False,
            output_attentions: bool = True
    ):
        """The __call__ function is the main function of a JAX module.
        It defines how the module behaves when called as a function, and it's what you'll use to call your model in practice.
        The __call__ method takes an input tensor (x) and returns an output tensor (y).
        In this case, we're defining our model to be a simple linear layer with no activation: y = x @ w + b.

        Args:
            self: Refer to the object itself
            hidden_states: chex.Array: Pass in the hidden state of the
                model
            freq_cis: Tuple[chex.Array, chex.Array],: Create the
                apply_rotary variable
            attention_mask: chex.Array: Mask the attention weights
            causal_mask: chex.Array: Mask the attention weights
            position_ids: chex.Array: Specify the position of each token
                in a sequence
            deterministic: bool: Determine whether to use dropout or not
            init_cache: bool: Initialize the cache
            output_attentions: bool: Determine whether to return the
                attention weights

        Returns:
            A tuple of (out, attn_output)
        """
        batch_size, sequence_length = hidden_states.shape[:2]
        query_states, key_states, value_states = self.q_proj(hidden_states), self.k_proj(hidden_states), self.v_proj(
            hidden_states)

        query_states = query_states.reshape(
            batch_size, sequence_length, self.config.num_attention_heads, self.head_dim
        )
        key_states = key_states.reshape(
            batch_size, sequence_length, self.config.num_key_value_heads, self.head_dim
        )
        value_states = value_states.reshape(
            batch_size, sequence_length, self.config.num_key_value_heads, self.head_dim
        )

        query_states, key_states, value_states = self.apply_rotary(
            query=query_states,
            key=key_states,
            value=value_states,
            position_ids=position_ids,
            freq_cis=freq_cis,
            batch_size=batch_size,
            sequence_length=sequence_length
        )

        query_length, key_length = query_states.shape[1], key_states.shape[1]

        if self.has_variable("cache", "cached_key"):
            mask_shift = self.variables["cache"]["cache_index"]
            max_decoder_length = self.variables["cache"]["cached_key"].shape[1]
            causal_mask = lax.dynamic_slice(
                causal_mask, (0, 0, mask_shift, 0), (1, 1,
                                                     query_length, max_decoder_length)
            )
        else:
            causal_mask = causal_mask[:, :, :query_length, :key_length]

        batch_size = hidden_states.shape[0]
        causal_mask = jnp.broadcast_to(
            causal_mask, (batch_size,) + causal_mask.shape[1:])
        attention_mask = jnp.broadcast_to(jnp.expand_dims(
            attention_mask, axis=(-3, -2)), causal_mask.shape)
        attention_mask = combine_masks(attention_mask, causal_mask)
        if attention_mask.ndim == 2:
            attention_mask = jnp.expand_dims(attention_mask, axis=(-3, -2))

        dropout_rng = None

        if not deterministic and self.config.attention_dropout > 0.0:
            dropout_rng = self.make_rng("dropout")

        if self.has_variable("cache", "cached_key") or init_cache:
            key_states, value_states, attention_mask = self._concatenate_to_cache(
                key_states,
                value_states,
                query_states,
                attention_mask
            )

        key_states, value_states = self.repeat_key_value(key_states, value_states, self.num_key_value_groups)
        assert_msg = (
            "num_attention_heads repeat wont work likely\n"
            f"INFO :\n\trepeat_key_values Used with num_key_value_groups = {self.num_key_value_groups}\n\t"
            f"NH : {self.config.num_attention_heads} KVH : {self.config.num_attention_heads}"
        )

        assert query_states.shape[-2] == self.config.num_attention_heads, assert_msg
        assert key_states.shape[-2] == self.config.num_attention_heads, assert_msg
        assert value_states.shape[-2] == self.config.num_attention_heads, assert_msg
        # if self.config.use_sharding_constraint:
        #     query_states = with_sharding_constraint(
        #         query_states, PartitionSpec(("dp", "fsdp"), "sp" if query_states.shape[1] != 1 else None, "tp", None)
        #     )
        #     key_states = with_sharding_constraint(
        #         key_states, PartitionSpec(("dp", "fsdp"), "sp", "tp", None)
        #     )
        #     value_states = with_sharding_constraint(
        #         value_states, PartitionSpec(("dp", "fsdp"), "sp", "tp", None)
        #     )
        attention_bias = lax.select(
            attention_mask > 0,
            jnp.full(attention_mask.shape, 0.0).astype(self.dtype),
            jnp.full(attention_mask.shape, jnp.finfo(
                self.dtype).min).astype(self.dtype),
        )

        query_length, key_length = query_states.shape[1], key_states.shape[1]

        attentions = self.attention_performer.__call__(
            query_states=query_states,
            key_states=key_states,
            value_states=value_states,
            bias=attention_bias,
            attention_mask=attention_mask,
            causal=True,
            dropout_rng=dropout_rng,
            deterministic=deterministic,
            query_sequence_length=query_length,
            key_value_sequence_length=key_length,
            uses_cache=self.has_variable("cache", "cached_key") or init_cache,
            segment_ids=segment_ids,
            causal_mask=causal_mask
        )

        attn_output = self._merge_heads(attentions.attention_outputs)
        if self.config.shard_attention_computation:
            attn_output = with_sharding_constraint(
                attn_output, PartitionSpec(
                    ("dp", "fsdp"),
                    "sp" if attn_output.shape[1] != 1 else None,
                    "tp"
                )
            )
        attn_output = self.o_proj(attn_output)
        outputs = (
            attn_output, attentions.attention_weights
        )
        return outputs


class ArcticMLP(nn.Module):
    config: ArcticConfig
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest")
    is_residual_mlp: bool = False

    def setup(self) -> None:
        config = self.config
        self.hidden_dim = config.hidden_size
        self.ffn_dim = config.intermediate_size if not self.is_residual_mlp else self.hidden_dim
        dense = functools.partial(
            Dense,
            use_bias=False,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision,
            kernel_init=nn.initializers.normal(),
            **get_dot_general_by_bits(self.config.bits, self.config.easy_method)
        )
        self.w1 = dense(self.ffn_dim)
        self.w3 = dense(self.ffn_dim)
        self.w2 = dense(self.hidden_dim)
        self.act_fn = ACT2FN[self.config.hidden_act]

    def __call__(self, x: chex.Array, e=None):
        x = control_mlp_sharding(x, self.config.partition_axis)
        return self.w2(self.act_fn(self.w1(x)) * self.w3(x))


class FlaxArcticBlocKSparesMLPCollection(nn.Module):
    config: ArcticConfig
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        self.layers = [
            ArcticMLP(
                config=self.config,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                precision=self.precision,
                name=str(i)
            )
            for i in range(self.config.num_local_experts)
        ]

    def __call__(
            self,
            selected_experts: chex.Array,
            hidden_states: chex.Array,
            routing_weights: chex.Array,
            batch_size: int,
            sequence_length: int,
            hidden_dim: int
    ) -> chex.Array:
        final_hidden_state = jnp.zeros_like(hidden_states)

        for index in range(self.config.num_local_experts):
            expert_layer_output = block_wise_ffn(
                self.layers[index],
                hidden_states,
                self.config.scan_mlp_chunk_size,
                False
            ) if self.config.use_scan_mlp else self.layers[index](hidden_states)
            expert_layer_output_exp = jnp.sum(
                jnp.multiply(
                    selected_experts == index, routing_weights
                ), axis=-1
            )[:, :, None] * expert_layer_output
            final_hidden_state += expert_layer_output_exp

        return final_hidden_state


class FlaxArcticMoE(nn.Module):
    config: ArcticConfig
    layer_id: int
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        config = self.config
        layer_id = self.layer_id
        self.hidden_dim = config.hidden_size
        self.num_experts = config.num_local_experts

        self.top_k = config.num_experts_per_tok
        self.is_moe_layer = (layer_id + 1) % config.moe_layer_frequency == 0

        if self.is_moe_layer:
            self.gate = Dense(
                self.config.num_local_experts,
                use_bias=False,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                precision=self.precision,
                kernel_init=nn.initializers.normal(),
            )
            self.experts = FlaxArcticBlocKSparesMLPCollection(
                config=self.config,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                precision=self.precision
            )
        else:
            self.mlp = ArcticMLP(
                config=config,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                precision=self.precision,
                is_residual_mlp=False
            )

    def _call_moe(
            self,
            hidden_states: chex.Array,
            e: bool = False  # Ignored
    ) -> Tuple[chex.Array, chex.Array]:

        hidden_states = control_mlp_sharding(hidden_states, self.config.partition_axis)
        batch_size, sequence_length, hidden_dim = hidden_states.shape

        router_logits = self.gate(hidden_states).astype(  # no reshaping is needed
            jnp.promote_types(self.dtype, jnp.float32)
        )
        routing_weights, selected_experts = jax.lax.top_k(
            router_logits,
            k=self.config.num_experts_per_tok
        )
        routing_weights = jax.nn.softmax(
            routing_weights.astype(
                jnp.promote_types(self.dtype, jnp.float32)
            ), axis=-1
        )

        return self.experts(
            selected_experts=selected_experts,
            batch_size=batch_size,
            sequence_length=sequence_length,
            hidden_dim=hidden_dim,
            hidden_states=hidden_states,
            routing_weights=routing_weights
        ), auxiliary_load_balancing_loss_func(
            (router_logits,),  # type:ignore
            self.num_experts,
            self.top_k,
            None
        )

    def __call__(self,
                 hidden_states: chex.Array,
                 e: bool = False  # Ignored
                 ):
        if self.is_moe_layer:
            return self._call_moe(hidden_states=hidden_states, e=e)
        return self.mlp(hidden_states, e=e), jnp.array(0.0, dtype=hidden_states.dtype)


class FlaxArcticSparseMoeBlock(nn.Module):
    """This implementation is
    strictly equivalent to standard MoE with full capacity (no
    dropped tokens). It's faster since it formulates MoE operations
    in terms of block-sparse operations to accomodate imbalanced
    assignments of tokens to experts, whereas standard MoE either
    (1) drop tokens at the cost of reduced performance or (2) set
    capacity factor to number of experts and thus waste computation
    and memory on padding.
    """
    config: ArcticConfig
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[
        Union[None, jax.lax.Precision]
    ] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        self.gate = Dense(
            self.config.num_local_experts,
            use_bias=False,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision,
            kernel_init=nn.initializers.normal(),
        )

        self.experts = FlaxArcticBlocKSparesMLPCollection(
            config=self.config,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision
        )

    def __call__(
            self,
            hidden_states: chex.Array,
            e: bool = False  # Ignored
    ) -> Tuple[chex.Array, chex.Array]:
        hidden_states = control_mlp_sharding(hidden_states, self.config.partition_axis)
        batch_size, sequence_length, hidden_dim = hidden_states.shape

        router_logits = self.gate(hidden_states).astype(  # no reshaping is needed
            jnp.promote_types(self.dtype, jnp.float32)
        )
        routing_weights, selected_experts = jax.lax.top_k(
            router_logits,
            k=self.config.num_experts_per_tok
        )
        routing_weights = jax.nn.softmax(
            routing_weights.astype(
                jnp.promote_types(self.dtype, jnp.float32)
            ), axis=-1
        )

        return self.experts(
            selected_experts=selected_experts,
            batch_size=batch_size,
            sequence_length=sequence_length,
            hidden_dim=hidden_dim,
            hidden_states=hidden_states,
            routing_weights=routing_weights
        ), router_logits


class FlaxArcticDecoderLayer(nn.Module):
    config: ArcticConfig
    layer_index: int
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[Union[str, jax.lax.Precision]] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        # hidden_states: chex.Array
        # freq_cis: Tuple[chex.Array, chex.Array],
        # attention_mask: chex.Array
        # causal_mask: chex.Array
        # position_ids: chex.Array
        # deterministic: bool = True
        # init_cache: bool = False
        # output_attentions: bool = True

        attn_block = FlaxArcticAttention
        mlp_block = FlaxArcticSparseMoeBlock
        if self.config.gradient_checkpointing != "":
            attn_block = re_mat(
                attn_block,
                policy=get_gradient_checkpoint_policy(self.config.gradient_checkpointing),
                static_argnums=(
                    1, 3, 4, 6, 7, 8, 9
                )
            )
            mlp_block = re_mat(
                mlp_block,
                policy=get_gradient_checkpoint_policy(self.config.gradient_checkpointing),
                static_argnums=(
                    1,
                )
            )
        self.self_attn = attn_block(
            config=self.config,
            layer_index=self.layer_index,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision
        )
        self.block_sparse_moe = mlp_block(
            config=self.config,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision
        )
        self.input_layernorm = ArcticRMSNorm(
            dim=self.config.hidden_size,
            eps=self.config.rms_norm_eps,
            dtype=self.dtype,
            param_dtype=self.param_dtype
        )
        self.post_attention_layernorm = ArcticRMSNorm(
            dim=self.config.hidden_size,
            eps=self.config.rms_norm_eps,
            dtype=self.dtype,
            param_dtype=self.param_dtype
        )
        self.parallel_attn_mlp_res = self.config.parallel_attn_mlp_res and self.block_sparse_moe.is_moe_layer
        if self.parallel_attn_mlp_res:
            self.residual_layernorm = ArcticRMSNorm(
                dim=self.config.hidden_size,
                eps=self.config.rms_norm_eps,
                dtype=self.dtype,
                param_dtype=self.param_dtype
            )
            self.residual_mlp = ArcticMLP(
                config=self.config,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                precision=self.precision,
                is_residual_mlp=True
            )

    def __call__(
            self,
            hidden_states: chex.Array,
            freq_cis: Tuple[chex.Array, chex.Array],
            attention_mask: chex.Array,
            causal_mask: chex.Array,
            position_ids: chex.Array,
            segment_ids: Optional[chex.Array] = None,
            deterministic: bool = True,
            init_cache: bool = False,
            output_attentions: bool = True,
    ):
        """The __call__ function is the main function of a TransformerEncoderLayer.
        It takes in the following arguments:
            hidden_states (chex.Array): The input to the encoder layer, which is also its output after being processed
            by all sublayers.
            freq_cis (chex.Array): A tensor containing frequency-domain representations of each token's context vector,
             used for computing self-attention weights and biases in a more efficient manner than using position
             embeddings or sinusoidal positional encoding vectors would allow

        Args:
            self: Represent the instance of the class
            hidden_states: chex.Array: Represent the input to the
                encoder layer
            freq_cis: Tuple[chex.Array, chex.Array],: Pass the frequency
                information to the attention layer
            attention_mask: chex.Array: Mask out the attention weights
                for certain positions
            causal_mask: chex.Array: Mask the future tokens
            position_ids: chex.Array: Indicate the position of each
                token in the sequence
            deterministic: bool: Determine whether to use dropout or not
            init_cache: bool: Initialize the cache for the self-
                attention layer

        Returns:
            A tuple of hidden_states and attention_output
        """
        residual_input = hidden_states
        hidden_states = self.input_layernorm(hidden_states)

        # hidden_states: chex.Array
        # freq_cis: Tuple[chex.Array, chex.Array],
        # attention_mask: chex.Array
        # causal_mask: chex.Array
        # position_ids: chex.Array
        # segment_ids: Optional[chex.Array] = None
        # deterministic: bool = True
        # init_cache: bool = False
        # output_attentions: bool = True

        hidden_states, self_attn_weights = self.self_attn(
            hidden_states,
            freq_cis,
            attention_mask,
            causal_mask,
            position_ids,
            segment_ids,
            deterministic,
            init_cache,
            output_attentions
        )

        hidden_states = residual_input + hidden_states

        residual_attn = hidden_states
        if self.parallel_attn_mlp_res:

            hidden_states = self.residual_layernorm(hidden_states)
            hidden_states = self.residual_mlp(hidden_states)
            residual_residual = residual_attn + hidden_states
            # parallel mlp moe part
            hidden_states = self.post_attention_layernorm(residual_input)
            hidden_states, gate_loss = self.block_sparse_moe(hidden_states)
            hidden_states = residual_residual + hidden_states
        else:
            hidden_states = self.post_attention_layernorm(hidden_states)
            hidden_states, gate_loss = self.block_sparse_moe(hidden_states)
            hidden_states = residual_attn + hidden_states

        outputs = (hidden_states,)
        if output_attentions:
            outputs += (self_attn_weights,)

        outputs += (gate_loss,)
        return outputs


class FlaxArcticDecoderLayerCollection(nn.Module):
    config: ArcticConfig
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        self.blocks = [
            FlaxArcticDecoderLayer(
                layer_index=layer_index,
                config=self.config,
                dtype=self.dtype,
                param_dtype=self.param_dtype,
                precision=self.precision,
                name=str(layer_index)
            )

            for layer_index in range(self.config.num_hidden_layers)
        ]

    def __call__(
            self,
            hidden_states: chex.Array,
            freq_cis: Tuple[chex.Array, chex.Array],
            attention_mask: chex.Array,
            causal_mask: chex.Array,
            position_ids: chex.Array,
            deterministic: bool = True,
            init_cache: bool = False,
            output_hidden_states: Optional[bool] = False,
            output_attentions: Optional[bool] = False,
    ):
        """The __call__ function is the main function of a TransformerEncoderLayer.
        It takes in the following arguments:
            hidden_states (chex.Array): The input to the encoder layer, which is also its output after being processed
             by all sublayers.
            freq_cis (chex.Array): A tensor containing frequency-domain representations of each token's context vector
            , used for computing self-attention weights and biases in a more efficient manner than using position
            embeddings or sinusoidal positional encoding vectors would allow for [2].

        Args:
            self: Represent the instance of the class
            hidden_states: chex.Array: Represent the input to the
                encoder layer
            freq_cis: Tuple[chex.Array, chex.Array],: Pass the frequency
                information to the attention layer
            attention_mask: chex.Array: Mask out the attention weights
                for certain positions
            causal_mask: chex.Array: Mask the future tokens
            position_ids: chex.Array: Indicate the position of each
                token in the sequence
            deterministic: bool: Determine whether to use dropout or not
            init_cache: bool: Initialize the cache for the self-
                attention layer
            output_attentions: bool: Determine whether to return the
                attention weights or not

        Returns:
            A tuple of hidden_states, attention_output,
            all_hidden_states and all_router_losses
        """
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        all_router_losses = ()
        for block in self.blocks:
            if output_hidden_states:
                all_hidden_states += (hidden_states,)
            layer_outputs = block(
                hidden_states=hidden_states,
                attention_mask=attention_mask,
                position_ids=position_ids,
                output_attentions=output_attentions,
                init_cache=init_cache,
                freq_cis=freq_cis,
                causal_mask=causal_mask,
                deterministic=deterministic,
            )

            hidden_states = layer_outputs[0]

            if output_attentions:
                all_self_attns += (layer_outputs[1],)

            all_router_losses += (layer_outputs[-1],)

        outputs = (hidden_states,)
        if output_attentions:
            outputs += (all_self_attns,)
        if output_hidden_states:
            outputs += (all_hidden_states,)
        outputs += (all_router_losses,)
        return outputs


class ArcticPreTrainedModel(EasyDeLFlaxPretrainedModel):
    config_class: ArcticConfig = ArcticConfig
    module_class: nn.Module = None
    base_model_prefix = "model"

    # main_input_name = "input_ids"

    def __init__(
            self,
            config: ArcticConfig,
            dtype: jnp.dtype = jnp.bfloat16,
            param_dtype: jnp.dtype = jnp.bfloat16,
            precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest"),
            input_shape: Tuple[int, int] = (1, 1),
            seed: int = 0,
            _do_init: bool = False,
            **kwargs
    ):
        module = self.module_class(
            config=config,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            **kwargs
        )

        super().__init__(
            dtype=dtype, _do_init=_do_init,
            module=module, config=config, input_shape=input_shape,
            seed=seed,
        )

    def init_weights(
            self,
            rng: jax.random.PRNGKey,
            input_shape: Tuple,
            params: FrozenDict = None
    ) -> FrozenDict:
        """The init_weights function is used to initialize the weights of a model.
        It takes in a rng, which is a random number generator key that can be used to generate random numbers.
        The input_shape parameter specifies the shape of the inputs that will be fed into this model.
        The params parameter allows you to pass in pre-trained weights for your model, if you have them available.

        Args:
            self: Access variables that belong to the class
            rng: jax.random.PRNGKey: Initialize the weights of the model
            input_shape: Tuple: Initialize the input_ids, attention_mask
                and position_ids
            params: flax.core.FrozenDict: Pass in the parameters of a
                pre-trained model

        Returns:
            A frozendict of parameters
        """

        self.config.initialization_of_moe = True
        input_ids = jnp.zeros(input_shape, dtype="i4")
        attention_mask = jnp.ones_like(input_ids, dtype="i4")
        position_ids = jnp.broadcast_to(
            jnp.arange(jnp.atleast_2d(input_ids).shape[-1], dtype="i4"),
            input_shape,
        )
        params_rng, dropout_rng = jax.random.split(rng)
        rngs = {"params": params_rng, "dropout": dropout_rng}
        if self.config.add_cross_attention:
            encoder_hidden_states = jnp.zeros(
                input_shape + (self.config.hidden_size,))
            encoder_attention_mask = attention_mask
            module_init_outputs = self.module.init(
                rngs,
                input_ids,
                attention_mask,
                position_ids,
                encoder_hidden_states,
                encoder_attention_mask,
                return_dict=False,
            )
        else:
            module_init_outputs = self.module.init(
                rngs,
                input_ids=input_ids,
                attention_mask=attention_mask,
                position_ids=position_ids,
                return_dict=False
            )
        random_params = module_init_outputs["params"]

        self.config.initialization_of_moe = False
        if params is not None:
            random_params = flatten_dict(unfreeze(random_params))
            params = flatten_dict(unfreeze(params))
            for missing_key in self._missing_keys:
                params[missing_key] = random_params[missing_key]
            self._missing_keys = set()
            return freeze(unflatten_dict(params))
        else:
            return random_params

    def init_cache(self, batch_size, max_length):

        input_ids = jnp.ones((batch_size, max_length))
        attention_mask = jnp.ones_like(input_ids)
        position_ids = jnp.broadcast_to(jnp.arange(
            jnp.atleast_2d(input_ids).shape[-1]), input_ids.shape)

        init_variables = self.module.init(
            jax.random.PRNGKey(0), input_ids, attention_mask, position_ids, return_dict=False, init_cache=True
        )
        return init_variables["cache"]

    def __call__(
            self,
            input_ids: chex.Array,
            attention_mask: Optional[chex.Array] = None,
            position_ids: Optional[chex.Array] = None,
            params: dict = None,
            past_key_values: dict = None,
            dropout_rng: jax.random.PRNGKey = None,
            train: bool = False,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
            add_params_field: bool = False,
            **kwargs
    ):
        """The __call__ function is the main function of a JAX module.
        It takes as input:
        - The parameters of the model (self.params)
        - The inputs to the model (input_ids, attention_mask, position_ids)
        - Whether we are training (train=True/False) and whether we want to return all hidden states and
        attentions weights at each layer in addition to just the last layer output (output_hidden_states=True/False).

        Args:
            self: Represent the instance of the class
            input_ids: Pass the input sequence to the model
            attention_mask: Mask out the padding tokens
            position_ids: Specify the position of each token in the
                sequence
            params: dict: Pass in the parameters of the model
            past_key_values: dict: Pass the past key values to the model
            dropout_rng: jax.random.PRNGKey: Pass in a random number
                generator key to the model
            train: bool: Determine whether to use dropout or not
            output_attentions: Optional[bool]: Determine whether to
                return the attention weights
            output_hidden_states: Optional[bool]: Determine whether to
                return the hidden states of all layers
            return_dict: Optional[bool]: Return a dictionary of the
                outputs
            add_params_field: bool: Add a params field to the inputs
                dictionary

        Returns:
            A tuple of (last_hidden_state, past_key_values)
        """

        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.return_dict

        batch_size, sequence_length = input_ids.shape

        if position_ids is None:
            if past_key_values is not None:
                raise ValueError(
                    "Make sure to provide `position_ids` when passing `past_key_values`.")

            position_ids = jnp.broadcast_to(jnp.arange(sequence_length)[
                                            None, :], (batch_size, sequence_length))

        if attention_mask is None:
            attention_mask = jnp.ones((batch_size, sequence_length))

        rng_s = {}
        if dropout_rng is not None:
            rng_s["dropout"] = dropout_rng

        inputs = {
            "params": params or self.params} if add_params_field else params or self.params

        if self.config.bits is not None:
            rng_s['params'] = jax.random.key(0)
        if past_key_values is not None:
            inputs["cache"] = past_key_values
            mutable = ["cache"]
        else:
            mutable = False

        outputs = self.module.apply(
            inputs,
            jnp.array(input_ids, dtype="i4"),  # input_ids: chex.Array
            # attention_mask: Optional[chex.Array] = None
            jnp.array(attention_mask, dtype="i4"),
            # position_ids: Optional[chex.Array] = None
            jnp.array(position_ids, dtype="i4"),
            None,  # inputs_embeds: Optional[chex.Array] = None
            output_attentions,  # output_attentions: Optional[bool] = None
            # output_hidden_states: Optional[bool] = None
            output_hidden_states,
            False,  # init_cache: bool = False
            not train,  # deterministic: bool = True
            return_dict,  # return_dict: bool = True
            rngs=rng_s,
            mutable=mutable,
        )

        if past_key_values is not None and return_dict:
            outputs, past_key_values = outputs
            outputs["past_key_values"] = unfreeze(past_key_values["cache"])
            return outputs
        elif past_key_values is not None and not return_dict:
            outputs, past_key_values = outputs
            outputs = outputs[:1] + \
                      (unfreeze(past_key_values["cache"]),) + outputs[1:]

        return outputs


class FlaxArcticModule(nn.Module):
    config: ArcticConfig
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        self.embed_tokens = nn.Embed(
            self.config.vocab_size,
            self.config.hidden_size,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
        )

        self.layers = FlaxArcticDecoderLayerCollection(
            config=self.config,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision
        )

        self.norm = ArcticRMSNorm(
            self.config.hidden_size,
            eps=self.config.rms_norm_eps,
            dtype=self.dtype,
            param_dtype=self.param_dtype
        )

        initial_rope_kwargs = dict(
            rope_type="none"
        )
        if self.config.rope_scaling is not None:
            scaling_type = self.config.rope_scaling["type"]
            scaling_factor = self.config.rope_scaling["factor"]
            initial_rope_kwargs = dict(
                scaling_factor=scaling_factor,
                rope_type=scaling_type
            )
        self.freq_cis = precompute_freq_cis(
            max_position_embeddings=(
                getattr(self.config, "freq_max_position_embeddings", self.config.max_position_embeddings)
            ),
            dim=self.config.hidden_size // self.config.num_attention_heads,
            base=self.config.rope_theta,
            **initial_rope_kwargs
        )
        self.causal_mask = flax.linen.make_causal_mask(
            jnp.ones(
                (1, getattr(self.config, "c_max_position_embeddings", self.config.max_position_embeddings)),
                dtype="bool"
            ), dtype="bool"
        )

    def __call__(
            self,
            input_ids: chex.Array,
            attention_mask: chex.Array,
            position_ids: chex.Array,
            inputs_embeds: Optional[chex.Array] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            init_cache: bool = False,
            deterministic: bool = True,
            return_dict: bool = True,
    ) -> MoeModelOutput | Tuple:
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError(
                "You cannot specify both decoder_input_ids and decoder_inputs_embeds at the same time")

        if inputs_embeds is None and input_ids is not None:
            inputs_embeds = self.embed_tokens(input_ids.astype("i4"))
        else:
            raise ValueError(
                "you should specify inputs_embeds or input_ids one of them")
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions

        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        collection_outputs = self.layers(
            hidden_states=inputs_embeds,
            attention_mask=attention_mask,
            position_ids=position_ids,
            causal_mask=self.causal_mask,
            freq_cis=self.freq_cis,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            init_cache=init_cache,
            deterministic=deterministic,
        )
        all_self_attns = None
        all_hidden_states = None
        hidden_states = collection_outputs[0]
        if output_attentions:
            all_self_attns = collection_outputs[1]
        if output_hidden_states:
            all_hidden_states = collection_outputs[2 if output_attentions else 1]

        all_router_losses = collection_outputs[-1]
        hidden_states = self.norm(hidden_states)

        if output_hidden_states:
            all_hidden_states += (hidden_states,)
        if not return_dict:
            return tuple(
                v
                for v in [hidden_states, all_hidden_states, all_self_attns, all_router_losses]
                if v is not None
            )
        return MoeModelOutput(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
            all_router_losses=all_router_losses,
        )


class FlaxArcticModel(ArcticPreTrainedModel):
    module_class = FlaxArcticModule

    def set_input_embeddings(self, value):
        self.module.embed_tokens = value

    def get_input_embeddings(self):
        return self.module.embed_tokens


class FlaxArcticForCausalLMModule(nn.Module):
    config: ArcticConfig
    dtype: jnp.dtype = jnp.bfloat16
    param_dtype: jnp.dtype = jnp.bfloat16
    precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest")

    def setup(self) -> None:
        self.model = FlaxArcticModule(
            config=self.config,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision
        )
        self.lm_head = Dense(
            self.config.vocab_size,
            dtype=self.dtype,
            param_dtype=self.param_dtype,
            precision=self.precision,
            use_bias=False,
            kernel_init=nn.initializers.normal(self.config.initializer_range),
            **get_dot_general_by_bits(self.config.bits, self.config.easy_method)
        )

    def __call__(
            self,
            input_ids: chex.Array,
            attention_mask: Optional[chex.Array] = None,
            position_ids: Optional[chex.Array] = None,
            inputs_embeds: Optional[chex.Array] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            init_cache: bool = False,
            deterministic: bool = True,
            return_dict: bool = True,
    ) -> MoeCausalLMOutput | Tuple:
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            init_cache=init_cache,
            deterministic=deterministic,
            return_dict=True,
        )
        logits = self.lm_head(outputs.last_hidden_state)

        aux_loss = sum(outputs[-1]) * self.config.router_aux_loss_coef
        if not return_dict:
            outputs = (logits,) + tuple(
                v
                for v in [
                    aux_loss,
                    outputs.hidden_states,
                    outputs.attentions,
                    outputs.all_router_losses
                ]
                if v is not None
            )
            return outputs

        return MoeCausalLMOutput(
            aux_loss=aux_loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            all_router_losses=outputs.all_router_losses,
        )


class FlaxArcticForCausalLM(ArcticPreTrainedModel):
    module_class = FlaxArcticForCausalLMModule

    def set_input_embeddings(self, value):
        self.module.model.embed_tokens = value

    def get_input_embeddings(self):
        return self.module.model.embed_tokens

    def set_decoder(self, decoder):
        self.module.model = decoder

    def get_decoder(self):
        return self.module.model

    def get_output_embeddings(self):
        return self.module.lm_head

    def set_output_embeddings(self, new_embeddings):
        self.module.lm_head = new_embeddings

    def prepare_inputs_for_generation(self, input_ids, max_length, attention_mask: Optional[chex.Array] = None):
        """The prepare_inputs_for_generation function is used to prepare the inputs for a generation task.

        Args:
            self: Access variables that belong to the class
            input_ids: Pass in the input tokens
            max_length: Set the length of the sequence to be generated
            attention_mask: Optional[chex.Array]: Mask the attention
                weights

        Returns:
            A dictionary of the past_key_values, attention_mask and
            position ids
        """
        batch_size, seq_length = input_ids.shape

        past_key_values = self.init_cache(batch_size, max_length)
        extended_attention_mask = jnp.ones(
            (batch_size, max_length), dtype="i4")
        if attention_mask is not None:
            position_ids = attention_mask.cumsum(axis=-1) - 1
            extended_attention_mask = lax.dynamic_update_slice(
                extended_attention_mask, attention_mask, (0, 0))
        else:
            position_ids = jnp.broadcast_to(jnp.arange(seq_length, dtype="i4")[
                                            None, :], (batch_size, seq_length))

        return {
            "past_key_values": past_key_values,
            "attention_mask": extended_attention_mask,
            "position_ids": position_ids,
        }

    def update_inputs_for_generation(self, model_outputs, model_kwargs):
        model_kwargs["past_key_values"] = model_outputs.past_key_values
        model_kwargs["position_ids"] = model_kwargs["position_ids"][:, -1:] + 1
        return model_kwargs
