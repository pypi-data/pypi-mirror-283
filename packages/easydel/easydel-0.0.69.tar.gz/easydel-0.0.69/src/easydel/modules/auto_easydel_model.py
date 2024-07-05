import functools
import gc
import re
import warnings
from functools import partial
from typing import Any, Callable, List, Mapping, Optional, Sequence, Tuple, Type

# import fjformer.linen.linen
import flax.traverse_util
import jax.numpy
from fjformer import make_shard_and_gather_fns, match_partition_rules
from flax.traverse_util import unflatten_dict
from jax.sharding import PartitionSpec
from transformers import AutoConfig, AutoModelForCausalLM

from easydel.etils.errors import EasyDeLRuntimeError
from easydel.etils.etils import get_logger
from easydel.etils.partition_module import PartitionAxis
from easydel.modules.easydel_modelling_utils import (
    EasyDeLFlaxPretrainedModel,
    EasyDeLPretrainedConfig,
)
from easydel.transform.easydel_transform import huggingface_to_easydel

logger = get_logger(name=__name__)


def get_modules_by_type(
    model_type: str,
) -> Tuple[
    Type[EasyDeLPretrainedConfig], Type[EasyDeLFlaxPretrainedModel] | Any, partial | Any
]:
    """
    The get_modules_by_type function is a helper function that returns the following:
        1. The config class for the model type specified (e.g., LlamaConfig, FalconConfig)
        2. The Flax Model class for the model type specified (e.g., FlaxLlamaForCausalLM, FlaxFalconForCausalLM)
        3. A function to convert a HuggingFace pretrained checkpoint into an easydel checkpoint

    :param model_type: str: Determine which model to use
    :return: A tuple of three elements (BaseConfig,BaseModel,Func To Transform Model from Torch to EasyDeL)

    """
    if model_type == "llama":
        from easydel.modules.llama import FlaxLlamaForCausalLM as _FlaxLlamaForCausalLM
        from easydel.modules.llama import LlamaConfig as _LlamaConfig

        return (
            _LlamaConfig,
            _FlaxLlamaForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "gemma":
        from easydel.modules.gemma import FlaxGemmaForCausalLM as _FlaxGemmaForCausalLM
        from easydel.modules.gemma import GemmaConfig as _GemmaConfig

        return (
            _GemmaConfig,
            _FlaxGemmaForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "gemma2":
        from easydel.modules.gemma2 import FlaxGemma2ForCausalLM as _FlaxGemma2ForCausalLM
        from easydel.modules.gemma2 import Gemma2Config as _Gemma2Config

        return (
            _Gemma2Config,
            _FlaxGemma2ForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "falcon":
        from easydel.modules.falcon import FalconConfig as _FalconConfig
        from easydel.modules.falcon import (
            FlaxFalconForCausalLM as _FlaxFalconForCausalLM,
        )

        return (
            _FalconConfig,
            _FlaxFalconForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["word_embeddings"],
                layer_norm_names=[
                    "input_layernorm",
                    "ln_f",
                    "ln_attn",
                    "ln_mlp",
                    "post_attention_layernorm",
                ],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "mpt":
        from easydel.modules.mosaic_mpt import FlaxMptForCausalLM as _FlaxMptForCausalLM
        from easydel.modules.mosaic_mpt import MptConfig as _MptConfig

        return (
            _MptConfig,
            _FlaxMptForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["wte"],
                rnn_based_or_rwkv=False,
                layer_norm_names=["norm_1", "norm_2", "norm_f"],
                lm_head_name="lm_head",
            ),
        )

    elif model_type == "mistral":
        from easydel.modules.mistral import (
            FlaxMistralForCausalLM as _FlaxMistralForCausalLM,
        )
        from easydel.modules.mistral import MistralConfig as _MistralConfig

        return (
            _MistralConfig,
            _FlaxMistralForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "gptj":
        from easydel.modules.gpt_j import FlaxGPTJForCausalLM as _FlaxGPTJForCausalLM
        from easydel.modules.gpt_j import GPTJConfig as _GPTJConfig

        return (
            _GPTJConfig,
            _FlaxGPTJForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names="wte",
                layer_norm_names=[
                    "ln_1",
                    "ln_2",
                    "ln_f",
                ],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )

    elif model_type == "gpt_neox":
        from easydel.modules.gpt_neo_x import (
            FlaxGPTNeoXForCausalLM as _FlaxGPTNeoXForCausalLM,
        )
        from easydel.modules.gpt_neo_x import GPTNeoXConfig as _GPTNeoXConfig

        return (
            _GPTNeoXConfig,
            _FlaxGPTNeoXForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names="wte",
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "palm":
        from easydel.modules.palm import FlaxPalmForCausalLM as _FlaxPalmForCausalLM
        from easydel.modules.palm import PalmConfig as _PalmConfig

        return (
            _PalmConfig,
            _FlaxPalmForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names="wte",
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "lt":
        from easydel.modules.lucid_transformer import FlaxLTConfig as _FlaxLTConfig
        from easydel.modules.lucid_transformer import (
            FlaxLTForCausalLM as _FlaxLTForCausalLM,
        )

        return (
            _FlaxLTConfig,
            _FlaxLTForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names="wte",
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "gpt2":
        from easydel.modules.gpt2 import FlaxGPT2LMHeadModel as _FlaxGPT2LMHeadModel
        from easydel.modules.gpt2 import GPT2Config as _GPT2Config

        return (
            _GPT2Config,
            _FlaxGPT2LMHeadModel,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["wte", "wpe"],
                layer_norm_names=["ln_1", "ln_2", "ln_f"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "mixtral":
        from easydel.modules.mixtral import (
            FlaxMixtralForCausalLM as _FlaxMixtralForCausalLM,
        )
        from easydel.modules.mixtral import MixtralConfig as _MixtralConfig

        return (
            _MixtralConfig,
            _FlaxMixtralForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "phi":
        from easydel.modules.phi import FlaxPhiForCausalLM as _FlaxPhiForCausalLM
        from easydel.modules.phi import PhiConfig as _PhiConfig

        return (
            _PhiConfig,
            _FlaxPhiForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                layer_norm_names=[
                    "input_layernorm",
                    "final_layernorm",
                    "q_layernorm",
                    "k_layernorm",
                ],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "qwen":
        from easydel.modules.qwen1 import FlaxQwen1ForCausalLM as _FlaxQwen1ForCausalLM
        from easydel.modules.qwen1 import Qwen1Config as _Qwen1Config

        return (
            _Qwen1Config,
            _FlaxQwen1ForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["wte"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )

    elif model_type == "qwen2":
        from easydel.modules.qwen2 import FlaxQwen2ForCausalLM as _FlaxQwen2ForCausalLM
        from easydel.modules.qwen2 import Qwen2Config as _Qwen2Config

        return (
            _Qwen2Config,
            _FlaxQwen2ForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "stablelm":
        from easydel.modules.stablelm import (
            FlaxStableLmForCausalLM as _FlaxStableLmForCausalLM,
        )
        from easydel.modules.stablelm import StableLmConfig as _StableLmConfig

        return (
            _StableLmConfig,
            _FlaxStableLmForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                layer_norm_names=[
                    "input_layernorm",
                    "post_attention_layernorm",
                    "norm",
                    "norms",
                ],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "rwkv":
        from easydel.modules.rwkv import FlaxRwkvForCausalLM as _FlaxRwkvForCausalLM
        from easydel.modules.rwkv import RwkvConfig as _RwkvConfig

        return (
            _RwkvConfig,
            _FlaxRwkvForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embeddings"],
                layer_norm_names=["ln_out", "ln2", "ln1", "pre_ln"],
                rnn_based_or_rwkv=True,
                lm_head_name="head",
            ),
        )
    elif model_type == "mamba":
        from easydel.modules.mamba import FlaxMambaForCausalLM as _FlaxMambaForCausalLM
        from easydel.modules.mamba import MambaConfig as _MambaConfig

        return (
            _MambaConfig,
            _FlaxMambaForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embeddings"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "grok-1":
        from easydel.modules.grok_1 import FlaxGrok1ForCausalLM as _FlaxGrok1ForCausalLM
        from easydel.modules.grok_1 import Grok1Config as _Grok1Config

        return (
            _Grok1Config,
            _FlaxGrok1ForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "qwen2_moe":
        from easydel.modules.qwen2_moe import (
            FlaxQwen2MoeForCausalLM as _FlaxQwen2MoeForCausalLM,
        )
        from easydel.modules.qwen2_moe import Qwen2MoeConfig as _Qwen2MoeConfig

        return (
            _Qwen2MoeConfig,
            _FlaxQwen2MoeForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "cohere":
        from easydel.modules.cohere import CohereConfig as _CohereConfig
        from easydel.modules.cohere import (
            FlaxCohereForCausalLM as _FlaxCohereForCausalLM,
        )

        return (
            _CohereConfig,
            _FlaxCohereForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "dbrx":
        from easydel.modules.dbrx import DbrxConfig as _DbrxConfig
        from easydel.modules.dbrx import FlaxDbrxForCausalLM as _FlaxDbrxForCausalLM

        return (
            _DbrxConfig,
            _FlaxDbrxForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["wte"],
                rnn_based_or_rwkv=False,
                layer_norm_names=["norm_1", "norm_2", "norm_f"],
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "phi3":
        from easydel.modules.phi3 import FlaxPhi3ForCausalLM as _FlaxPhi3ForCausalLM
        from easydel.modules.phi3 import Phi3Config as _Phi3Config

        return (
            _Phi3Config,
            _FlaxPhi3ForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )

    elif model_type == "arctic":
        from easydel.modules.arctic import ArcticConfig as _ArcticConfig
        from easydel.modules.arctic import (
            FlaxArcticForCausalLM as _FlaxArcticForCausalLM,
        )

        return (
            _ArcticConfig,
            _FlaxArcticForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "openelm":
        from easydel.modules.openelm import (
            FlaxOpenELMForCausalLM as _FlaxOpenELMForCausalLM,
        )
        from easydel.modules.openelm import OpenELMConfig as _OpenELMConfig

        return (
            _OpenELMConfig,
            _FlaxOpenELMForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["token_embeddings"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "deepseek_v2":
        from easydel.modules.deepseek_v2 import DeepseekV2Config as _DeepseekV2Config
        from easydel.modules.deepseek_v2 import (
            FlaxDeepseekV2ForCausalLM as _FlaxDeepseekV2ForCausalLM,
        )

        return (
            _DeepseekV2Config,
            _FlaxDeepseekV2ForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    elif model_type == "olmo":
        from easydel.modules.olmo import FlaxOlmoForCausalLM as _FlaxOlmoForCausalLM
        from easydel.modules.olmo import OlmoConfig as _OlmoConfig

        return (
            _OlmoConfig,
            _FlaxOlmoForCausalLM,
            functools.partial(
                huggingface_to_easydel,
                embedding_layer_names=["embed_tokens"],
                rnn_based_or_rwkv=False,
                lm_head_name="lm_head",
            ),
        )
    raise EasyDeLRuntimeError(
        f"Model Type ({model_type}) is not supported or is not found"
    )


def is_flatten(pytree: dict):
    """The is_flatten function checks if the pytree is flattened.
        If it is, then the first key in the dictionary will be a tuple of (mpl, mpl_id).
        Otherwise, it will be an integer representing mpl_id.

    Args:
        pytree: dict: Pass the pytree to the function

    Returns:
        True if the pytree is a flattened tree, and false otherwise
    """
    mpl = [k for k in pytree.keys()][0]
    return True if isinstance(mpl, tuple) else False


class AutoEasyDeLModelForCausalLM:
    """This class provides a convenient way to load and shard pretrained causal language models from the Hugging Face Hub
    and convert them into EasyDeL compatible models. It utilizes the EasyDeL library for distributed training and inference
    with JAX.

    This class inherits from the `EasyDeLFlaxPretrainedModel` class, providing functionalities for model loading,
    parameter sharding, and interaction with the EasyDeL framework.

    Attributes:
        None

    Examples:
        ```python
        import jax
        from easydel import AutoEasyDeLModelForCausalLM

        # Load a GPT-2 model on a single CPU
        model, params = AutoEasyDeLModelForCausalLM.from_pretrained(
            "gpt2",
            device=jax.devices("cpu")[0]
        )

        # Load a GPT-2 model sharded across 8 GPUs with data parallelism (DP) and fully sharded data parallelism (FSDP)
        model, params = AutoEasyDeLModelForCausalLM.from_pretrained(
            "gpt2",
            sharding_axis_dims=(1, 8, 1, 1),
            sharding_axis_names=("dp", "fsdp", "tp", "sp"),
            device=jax.devices("cpu")[0], # offload to CPU [OPTIONAL]
            from_torch=True,
        )
        ```
    """

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: str,
        device=jax.devices("cpu")[0],
        dtype: jax.numpy.dtype = jax.numpy.float32,
        param_dtype: jax.numpy.dtype = jax.numpy.float32,
        precision: Optional[jax.lax.Precision] = jax.lax.Precision("fastest"),
        sharding_axis_dims: Sequence[int] = (1, -1, 1, 1),
        sharding_axis_names: Sequence[str] = ("dp", "fsdp", "tp", "sp"),
        partition_axis: PartitionAxis = PartitionAxis(),
        shard_attention_computation: bool = True,
        input_shape: Tuple[int, int] = (1, 1),
        shard_fns: Optional[Mapping[tuple, Callable] | dict] = None,
        backend: Optional[str] = None,
        config_kwargs: Optional[Mapping[str, Any]] = None,
        auto_shard_params: bool = False,
        partition_rules: Optional[Tuple[Tuple[str, PartitionSpec], ...]] = None,
        load_in_8bit: bool = False,
        bit_targeted_params: Optional[List[str]] = None,
        verbose_params: bool = False,
        safe: bool = True,
        from_torch: bool = True,
        **kwargs,
    ) -> Tuple[EasyDeLFlaxPretrainedModel, dict]:
        """Loads and shards a pretrained causal language model from the Hugging Face Hub and converts it into an
        EasyDeL compatible model.

        Args:
            pretrained_model_name_or_path (str): Path or name of the pretrained model in the Hugging Face Hub.
            device (jax.Array, optional): Device to load the model on. Defaults to the first CPU.
            dtype (jax.numpy.dtype, optional): Data type of the model. Defaults to jax.numpy.float32.
            param_dtype (jax.numpy.dtype, optional): Data type of the model parameters. Defaults to jax.numpy.float32.
            precision (jax.lax.Precision, optional): Precision for computations. Defaults to jax.lax.Precision("fastest").
            sharding_axis_dims (Sequence[int], optional): Dimensions of each sharding axis. Defaults to (1, -1, 1, 1).
            sharding_axis_names (Sequence[str], optional): Names of the sharding axes. Defaults to ("dp", "fsdp", "tp", "sp").
            partition_axis (PartitionAxis) : PartitionAxis is new module used for partitioning arrays in easydel.
            shard_attention_computation (bool, optional): Whether to shard attention computation. Defaults to True.
            input_shape (Tuple[int, int], optional): Shape of the input to the model. Defaults to (1, 1).
            shard_fns (Optional[Mapping[tuple, Callable] | dict], optional): Sharding functions to use for the model. If None,
                auto-sharding is used if auto_shard_params is True. Defaults to None.
            backend (Optional[str], optional): Backend to use for the model. Defaults to None.
            config_kwargs (Optional[Mapping[str, Any]], optional): Configuration keyword arguments to pass to the model config.
                Defaults to None.
            auto_shard_params (bool, optional): Whether to automatically shard the model parameters. Defaults to False.
            partition_rules (Optional[Tuple[Tuple[str, PartitionSpec]]], optional): Custom partition rules for parameter
                sharding. If not None, shard_fns should also be provided. Defaults to None.
            load_in_8bit (bool, optional): Whether to load the model parameters in 8-bit precision. Defaults to False.
            bit_targeted_params (Optional[List[str]], optional): List of parameter names to convert to 8-bit precision. If
                None and load_in_8bit is True, all kernels and embeddings are converted to 8-bit. Defaults to None.
            verbose_params (bool): whenever to log number of parameters in converting state.
            safe (bool): whenever to use safetensors to load engine or parameters (requires engine or parameters to be saved with safe=True while saving them)
            from_torch (bool): whenever to load the model from transformers-pytorch.
            **kwargs: Additional keyword arguments to pass to the model and config classes.

        Returns:
            Tuple[EasyDeLFlaxPretrainedModel, dict]: A tuple containing the EasyDeL model and the loaded and sharded
                model parameters.
        """
        if from_torch:
            return cls._from_torch(
                pretrained_model_name_or_path=pretrained_model_name_or_path,
                param_dtype=param_dtype,
                dtype=dtype,
                shard_fns=shard_fns,
                auto_shard_params=auto_shard_params,
                precision=precision,
                backend=backend,
                verbose_params=verbose_params,
                partition_axis=partition_axis,
                load_in_8bit=load_in_8bit,
                partition_rules=partition_rules,
                bit_targeted_params=bit_targeted_params,
                sharding_axis_names=sharding_axis_names,
                sharding_axis_dims=sharding_axis_dims,
                input_shape=input_shape,
                config_kwargs=config_kwargs,
                device=device,
                shard_attention_computation=shard_attention_computation,
                **kwargs,
            )
        with jax.default_device(device):
            return cls._from_easydel_params(
                auto_shard_params=auto_shard_params,
                input_shape=input_shape,
                partition_axis=partition_axis,
                sharding_axis_dims=sharding_axis_dims,
                sharding_axis_names=sharding_axis_names,
                shard_fns=shard_fns,
                param_dtype=param_dtype,
                config_kwargs=config_kwargs,
                partition_rules=partition_rules,
                precision=precision,
                dtype=dtype,
                pretrained_model_name_or_path=pretrained_model_name_or_path,
                safe=safe,
            )

    @staticmethod
    def _from_torch(
        pretrained_model_name_or_path,
        device,
        dtype: jax.numpy.dtype,
        param_dtype: jax.numpy.dtype,
        precision: Optional[jax.lax.Precision],
        sharding_axis_dims: Sequence[int],
        sharding_axis_names: Sequence[str],
        partition_axis: PartitionAxis,
        shard_attention_computation: bool,
        input_shape: Tuple[int, int],
        shard_fns: Optional[Mapping[tuple, Callable] | dict],
        backend: Optional[str],
        config_kwargs: Optional[Mapping[str, Any]],
        auto_shard_params: bool,
        partition_rules: Optional[Tuple[Tuple[str, PartitionSpec], ...]],
        load_in_8bit: bool,
        bit_targeted_params: Optional[List[str]],
        verbose_params: bool,
        **kwargs,
    ):
        try:
            import torch

            if torch.cuda.is_available():

                def _clear():
                    gc.collect()
                    torch.cuda.empty_cache()

            else:

                class torch:
                    bfloat16 = None

                def _clear():
                    gc.collect()

        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "in order to load model from torch you should install torch first "
                "run `pip install torch`"
            )

        logger.debug(f"Downloading model config from {pretrained_model_name_or_path}")
        config = AutoConfig.from_pretrained(pretrained_model_name_or_path)
        model_type: str = config.model_type

        cfg, module, trf = get_modules_by_type(model_type)

        logger.debug(f"Downloading model weights from {pretrained_model_name_or_path}")
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path, **kwargs
        )
        if verbose_params:
            print(
                f"PyTorch - HF Model contains {sum(p.numel() for p in model.parameters()) / 1e9} Billion Parameters"
            )
        cfg = cfg.from_pretrained(pretrained_model_name_or_path)
        state_dict = model.state_dict()

        # Clear and collect memory after deleting the model
        del model
        _clear()

        logger.debug("adding model basic EasyDeL configurations.")
        if hasattr(cfg, "add_jax_args"):
            cfg.add_jax_args()
        cfg.add_basic_configurations(
            axis_dims=sharding_axis_dims,
            axis_names=sharding_axis_names,
            partition_axis=partition_axis,
            backend=backend,
            shard_attention_computation=shard_attention_computation,
        )
        if config_kwargs is not None:
            for k, v in config_kwargs.items():
                setattr(cfg, k, v)
        logger.debug("creating easydel model")
        ed_model = module(
            config=cfg,
            _do_init=False,
            dtype=dtype,
            param_dtype=param_dtype,
            precision=precision,
            input_shape=input_shape,
        )

        needs = [
            s.replace(".kernel", ".weight")
            .replace(".scale", ".weight")
            .replace(".embedding", ".weight")
            for s in list(
                flax.traverse_util.flatten_dict(
                    ed_model.params_shape_tree, sep="."
                ).keys()
            )
        ]
        for k in list(state_dict.keys()):
            if k not in needs:
                tensor = state_dict.pop(k)
                del tensor
                _clear()
                logger.debug(
                    f"removing {k} from weights as it was not needed by flax model"
                )

        _clear()

        if shard_fns is not None:
            if auto_shard_params:
                warnings.warn(
                    "`auto_shard_params` will be ignored since you are passing custom sharding functions"
                )
            logger.debug("sharding model parameters based on the given shard_fns.")
            if not is_flatten(shard_fns):
                shard_fns = flax.traverse_util.flatten_dict(shard_fns)
        elif auto_shard_params:
            shard_fns, _ = AutoShardAndGatherFunctions.from_pretrained(
                pretrained_model_name_or_path=pretrained_model_name_or_path,
                partition_rules=partition_rules,
                sharding_axis_dims=sharding_axis_dims,
                sharding_axis_names=sharding_axis_names,
                partition_axis=partition_axis,
                shard_attention_computation=shard_attention_computation,
                backend=backend,
                input_shape=input_shape,  # type:ignore
                config_kwargs=config_kwargs,
            )
        logger.debug("converting huggingface-model to easydel-model.")
        params_pattern_selection = None
        if load_in_8bit:
            if bit_targeted_params is None:
                warnings.warn(
                    "since `bit_targeted_params` is set to None, auto loader will convert all of"
                    " kernels(weights) and embeddings to 8bit by default"
                )
                bit_targeted_params = ["kernel", "embedding"]

                params_pattern_selection = re.compile(
                    "({})".format("|".join(bit_targeted_params))
                )
        uses_tie_word_embedding = getattr(config, "tie_word_embeddings", False)
        params = trf(
            state_dict,
            config=config,
            device=device,
            shard_fns=shard_fns,
            convert_to_8bit=load_in_8bit,
            params_pattern_selection=params_pattern_selection,
            remove_state_dict=True,
            uses_tie_word_embedding=uses_tie_word_embedding,
            dtype=param_dtype,
        )

        # Clear and collect memory after converting the model
        del state_dict
        _clear()

        if is_flatten(params):
            logger.info("converted parameters are flatten making them unflatten ")
            params = unflatten_dict(params)

        if verbose_params:
            print(
                f"JAX - EasyDeL Model contains "
                f"{sum(n.size for n in jax.tree_util.tree_flatten(flax.core.unfreeze(params))[0]) / 1e9}"
                f" Billion Parameters"
            )
        return ed_model, params

    @staticmethod
    def _from_easydel_params(
        pretrained_model_name_or_path,
        dtype: jax.numpy.dtype,
        param_dtype: jax.numpy.dtype,
        precision: Optional[jax.lax.Precision],
        sharding_axis_dims: Sequence[int],
        sharding_axis_names: Sequence[str],
        partition_axis: PartitionAxis,
        input_shape: Tuple[int, int],
        shard_fns: Optional[Mapping[tuple, Callable] | dict],
        config_kwargs: Optional[Mapping[str, Any]],
        auto_shard_params: bool,
        partition_rules: Optional[Tuple[Tuple[str, PartitionSpec], ...]],
        safe: bool,
        # load_in_8bit: bool,
        # bit_targeted_params: Optional[List[str]],
    ):
        from easydel.modules.easydel_modelling_utils import EasyDeLFlaxPretrainedModel

        return EasyDeLFlaxPretrainedModel.from_pretrained(
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            input_shape=input_shape,
            dtype=dtype,
            precision=precision,
            param_dtype=param_dtype,
            partition_axis=partition_axis,
            auto_shard_params=auto_shard_params,
            shard_fns=shard_fns,
            sharding_axis_dims=sharding_axis_dims,
            sharding_axis_names=sharding_axis_names,
            config_kwargs=config_kwargs,
            partition_rules=partition_rules,
            safe=safe,
        )


class AutoEasyDeLConfig:
    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: str,
        sharding_axis_dims: Sequence[int] = (1, -1, 1, 1),
        sharding_axis_names: Sequence[str] = ("dp", "fsdp", "tp", "sp"),
        partition_axis: PartitionAxis = PartitionAxis(),
        shard_attention_computation: bool = True,
        backend: Optional[str] = None,
        from_torch: bool = False,
        **kwargs,
    ) -> EasyDeLPretrainedConfig:
        """The from_pretrained function is a helper function that allows you to instantiate a model from the pretrained
        model repository. It takes as input the name of the model (e.g., 'bert-base-uncased') and returns an instance of
        the class corresponding to your model, with all weights loaded from disk.

        Args:
            cls: Create an instance of the class that called this function
            pretrained_model_name_or_path: str: Identify the model in the huggingface model hub
            sharding_axis_dims: Sequence[int]: Specify the dimension of each axis in the sharded model
            sharding_axis_names: Sequence[str]: Specify the order of sharding
            partition_axis (PartitionAxis) : PartitionAxis is new module used for partitioning arrays in easydel.
            shard_attention_computation: bool: whenever to use shard_map for attention
            backend: Optional[str]: backend to use for model
            from_torch: should config be loaded from torch models or not.
            **kwargs: Pass additional arguments to the model and config classes
        generation process

        Returns:
            A Model Config
        """
        cls_main = AutoConfig if from_torch else EasyDeLPretrainedConfig
        config = cls_main.from_pretrained(pretrained_model_name_or_path)
        model_type: str = config.model_type

        cfg, module, trf = get_modules_by_type(model_type)
        cfg = cfg.from_pretrained(pretrained_model_name_or_path)
        if hasattr(cfg, "add_jax_args"):
            cfg.add_jax_args()
        cfg.add_basic_configurations(
            axis_dims=sharding_axis_dims,
            axis_names=sharding_axis_names,
            partition_axis=partition_axis,
            backend=backend,
            shard_attention_computation=shard_attention_computation,
        )

        return cfg


class AutoShardAndGatherFunctions:
    """
    A class to automatically generate shard and gather functions for a given model configuration.

    This class provides two methods to generate shard and gather functions:

    - `from_config`: Generates functions based on a provided `EasyDeLPretrainedConfig` object.
    - `from_pretrained`: Generates functions based on a pretrained model name or path.

    Attributes:
        None

    Methods:
        from_config: Generates shard and gather functions based on a provided `EasyDeLPretrainedConfig` object.
        from_pretrained: Generates functions based on a pretrained model name or path.
    """

    @classmethod
    def from_config(
        cls,
        config: EasyDeLPretrainedConfig,
        partition_rules: Optional[Tuple[Tuple[str, PartitionSpec]]] = None,
        flatten: bool = True,
        input_shape: Tuple[int, int] = (1, 1),
        depth_target: Optional[List[str]] = None,
    ):
        """
        Generates shard and gather functions based on a provided `EasyDeLPretrainedConfig` object.

        Args:
            config: An `EasyDeLPretrainedConfig` object containing the model configuration.
            partition_rules: A tuple of tuples containing partition rule names and `PartitionSpec` objects.
                If None, uses the default partition rules from the `config`.
            flatten: Whether to flatten the shard and gather functions. Defaults to True.
            input_shape: The input shape of the model. Defaults to (1, 1).
            depth_target: Pad the sharding to depth, for example make {params:tensor} with depth_target = ["row"] to {row:{params:tensor}}. Defaults to None.

        Returns:
            A tuple containing the shard and gather functions.
        """
        if partition_rules is None:
            warnings.warn(
                "Using config partition rules from `get_partition_rules(fully_sharded_data_parallel=True)`"
            )
            partition_rules = config.get_partition_rules(True)
        _, module, _ = get_modules_by_type(config.model_type)
        model = module(config=config, _do_init=False, input_shape=input_shape)

        partition_specs = match_partition_rules(
            partition_rules, model.params_shape_tree
        )
        shard_fns, gather_fns = make_shard_and_gather_fns(
            partition_specs=partition_specs,
            mesh=config.get_mesh(),
        )
        if depth_target is not None:
            for dp in depth_target[::-1]:
                gather_fns = {dp: gather_fns}
                shard_fns = {dp: shard_fns}
        if flatten and not is_flatten(shard_fns):
            gather_fns = flax.traverse_util.flatten_dict(gather_fns)
            shard_fns = flax.traverse_util.flatten_dict(shard_fns)
        elif not flatten and is_flatten(shard_fns):
            gather_fns = flax.traverse_util.unflatten_dict(gather_fns)
            shard_fns = flax.traverse_util.unflatten_dict(shard_fns)

        return shard_fns, gather_fns

    @staticmethod
    def from_params(params, partition_rules, mesh):
        partition_specs = match_partition_rules(partition_rules, params)
        return make_shard_and_gather_fns(
            partition_specs=partition_specs,
            mesh=mesh,
        )

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: str,
        input_shape: Tuple[int, int] = (1, 1),
        sharding_axis_dims: Sequence[int] = (1, -1, 1, 1),
        sharding_axis_names: Sequence[str] = ("dp", "fsdp", "tp", "sp"),
        partition_axis: PartitionAxis = PartitionAxis(),
        shard_attention_computation: bool = True,
        backend: Optional[str] = None,
        partition_rules: Optional[Tuple[Tuple[str, PartitionSpec]]] = None,
        flatten: bool = True,
        config_kwargs: Optional[Mapping[str, Any]] = None,
        depth_target: Optional[List[str]] = None,
        from_torch: bool = False,
    ) -> Tuple[Mapping[str, Callable], Mapping[str, Callable]]:
        """
        Generates shard and gather functions based on a pretrained model name or path.

        Args:
            pretrained_model_name_or_path: The name or path of the pretrained model.
            input_shape: The input shape of the model. Defaults to (1, 1).
            sharding_axis_dims: The dimensions of the sharding axes. Defaults to (1, -1, 1, 1).
            sharding_axis_names: The names of the sharding axes. Defaults to ("dp", "fsdp", "tp", "sp").
            partition_axis (PartitionAxis) : PartitionAxis is new module used for partitioning arrays in easydel.
            shard_attention_computation: Whether to shard the attention computation. Defaults to True.
            backend: The backend to use for sharding. Defaults to None.
            partition_rules: A tuple of tuples containing partition rule names and `PartitionSpec` objects.
                If None, uses the default partition rules from the `config`.
            flatten: Whether to flatten the shard and gather functions. Defaults to True.
            config_kwargs: Additional keyword arguments to pass to the `AutoEasyDeLConfig` constructor. Defaults to None.
            depth_target: Pad the sharding to depth, for example make {params:tensor} with depth_target = ["row"] to {row:{params:tensor}}. Defaults to None.
            from_torch: should config be loaded from torch models or not.
        Returns:
            A tuple containing the shard and gather functions.
        """
        config = AutoEasyDeLConfig.from_pretrained(
            pretrained_model_name_or_path,
            sharding_axis_dims=sharding_axis_dims,
            sharding_axis_names=sharding_axis_names,
            partition_axis=partition_axis,
            shard_attention_computation=shard_attention_computation,
            backend=backend,
            from_torch=from_torch,
        )
        if config_kwargs is not None:
            for k, v in config_kwargs.items():
                setattr(config, k, v)
        return cls.from_config(
            config=config,
            partition_rules=partition_rules,
            flatten=flatten,
            input_shape=input_shape,
            depth_target=depth_target,
        )
