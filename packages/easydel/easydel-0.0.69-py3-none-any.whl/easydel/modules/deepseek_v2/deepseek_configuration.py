import warnings
from typing import Optional, Dict, Union

from jax.sharding import PartitionSpec

from easydel.modules.easydel_modelling_utils import EasyDeLPretrainedConfig


class DeepseekV2Config(EasyDeLPretrainedConfig):
    model_type: str = "deepseek_v2"

    def __init__(
            self,
            vocab_size=102400,
            hidden_size=4096,
            intermediate_size=11008,
            moe_intermediate_size=1407,
            num_hidden_layers=30,
            num_attention_heads=32,
            num_key_value_heads=32,
            n_shared_experts=None,
            n_routed_experts=None,
            ep_size=1,
            routed_scaling_factor=1.0,
            kv_lora_rank=512,
            q_lora_rank=1536,
            qk_rope_head_dim=64,
            v_head_dim=128,
            qk_nope_head_dim=128,
            topk_method='gready',
            n_group=None,
            topk_group=None,
            num_experts_per_tok=None,
            moe_layer_freq=1,
            first_k_dense_replace=0,
            norm_topk_prob=False,
            scoring_func='softmax',
            aux_loss_alpha=0.001,
            seq_aux=True,
            hidden_act="silu",
            max_position_embeddings=2048,
            initializer_range=0.02,
            rms_norm_eps=1e-6,
            use_cache=True,
            pad_token_id=None,
            bos_token_id=100000,
            eos_token_id=100001,
            pretraining_tp=1,
            tie_word_embeddings=False,
            rope_theta=10000.0,
            attention_bias=False,
            attention_dropout=0.0,
            gradient_checkpointing: str = "nothing_saveable",
            use_scan_mlp: bool = False,
            scan_mlp_chunk_size: int = 1024,
            bits: Optional[int] = None,
            rope_scaling: Dict[str, Union[str, float]] = None,
            **kwargs,
    ):
        warnings.warn(
            "`DeepseekV2` is still in beta mode.",
            UserWarning
        )
        self.vocab_size = vocab_size
        self.max_position_embeddings = max_position_embeddings
        self.hidden_size = hidden_size
        self.intermediate_size = intermediate_size
        self.moe_intermediate_size = moe_intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.n_shared_experts = n_shared_experts
        self.n_routed_experts = n_routed_experts
        self.ep_size = ep_size
        self.routed_scaling_factor = routed_scaling_factor
        self.kv_lora_rank = kv_lora_rank
        self.q_lora_rank = q_lora_rank
        self.qk_rope_head_dim = qk_rope_head_dim
        self.v_head_dim = v_head_dim
        self.qk_nope_head_dim = qk_nope_head_dim
        self.topk_method = topk_method
        self.n_group = n_group
        self.topk_group = topk_group
        self.num_experts_per_tok = num_experts_per_tok
        self.moe_layer_freq = moe_layer_freq
        self.first_k_dense_replace = first_k_dense_replace
        self.norm_topk_prob = norm_topk_prob
        self.scoring_func = scoring_func
        self.aux_loss_alpha = aux_loss_alpha
        self.seq_aux = seq_aux
        # for backward compatibility
        if num_key_value_heads is None:
            num_key_value_heads = num_attention_heads

        self.num_key_value_heads = num_key_value_heads
        self.hidden_act = hidden_act
        self.initializer_range = initializer_range
        self.rms_norm_eps = rms_norm_eps
        self.pretraining_tp = pretraining_tp
        self.use_cache = use_cache
        self.rope_theta = rope_theta
        self.rope_scaling = rope_scaling
        self.attention_bias = attention_bias
        self.attention_dropout = attention_dropout
        self.gradient_checkpointing = gradient_checkpointing
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            tie_word_embeddings=tie_word_embeddings,
            use_scan_mlp=use_scan_mlp,
            scan_mlp_chunk_size=scan_mlp_chunk_size,
            bits=bits,
            **kwargs,
        )

    def get_partition_rules(self, fully_sharded_data_parallel: bool = True):
        """The get_partition_rules function is used to define the partitioning scheme for a model.
        It returns a list of tuples, where each tuple contains two elements:
          1) A regex string that matches the name of one or more parameters in the model.
          2) A PartitionScheme object that defines how those parameters should be partitioned.

        Args:
            fully_sharded_data_parallel: bool: Determine whether to use
                the fully_sharded_data_parallel partitioning scheme or
                not

        Returns:
            A list of tuples
        """
        return (

            ("model/embed_tokens/embedding", PartitionSpec("sp", "fsdp")),

            ("self_attn/(q_proj|k_proj|v_proj)/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
            ("self_attn/o_proj/kernel", PartitionSpec("tp", ("sp", "fsdp"))),

            ("w1/kernel", PartitionSpec(("fsdp", "sp"))),
            ("w2/kernel", PartitionSpec(("fsdp", "sp"))),
            ("w3/kernel", PartitionSpec(("fsdp", "sp"))),
            ("gate/kernel", PartitionSpec(("fsdp", "sp"))),

            ("input_layernorm/kernel", PartitionSpec(None)),
            ("post_attention_layernorm/kernel", PartitionSpec(None)),

            ("model/norm/kernel", PartitionSpec(None)),
            ("lm_head/kernel", PartitionSpec("fsdp", "sp")),
            (".*", PartitionSpec(None)),
        ) if not fully_sharded_data_parallel else (
            ("model/embed_tokens/embedding", PartitionSpec(("fsdp", "sp"))),

            ("self_attn/(q_proj|k_proj|v_proj)/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
            ("self_attn/o_proj/kernel", PartitionSpec("tp", ("sp", "fsdp"))),

            ("w1/kernel", PartitionSpec(("fsdp", "sp"))),
            ("w2/kernel", PartitionSpec(("fsdp", "sp"))),
            ("w3/kernel", PartitionSpec(("fsdp", "sp"))),
            ("gate/kernel", PartitionSpec(("fsdp", "sp"))),

            ("input_layernorm/kernel", PartitionSpec(None)),
            ("post_attention_layernorm/kernel", PartitionSpec(None)),

            ("model/norm/kernel", PartitionSpec(None)),
            ("lm_head/kernel", PartitionSpec(("fsdp", "sp"))),
            (".*", PartitionSpec(("fsdp", "sp"))),
        )

    def add_jax_args(
            self,
            gradient_checkpointing: str = "nothing_saveable",
            use_scan_mlp: bool = False,
            scan_mlp_chunk_size: int = 1024,
            bits: Optional[int] = None,
            rope_scaling: Dict[str, Union[str, float]] = None,
            **kwargs,
    ):
        """The add_jax_args function adds the following arguments to the model:

        Args:
            self: Bind the attributes and methods of a class to an
                instance of that class
            gradient_checkpointing: str: Determine whether to use
                gradient checkpointing
            use_scan_mlp: bool: Determine whether to use the scan_mlp
                function or not
            scan_mlp_chunk_size: int: Chunk the input to the mlp
            number_rep_kv: int: Control the number of times that the key
                and value vectors are repeated
            bits: Optional[int]: Specify the number of bits to use for
                quantization
            attention_dropout: float: Set the dropout rate for the
                attention layer
            attention_bias: bool: when ever to use attention_bias
            initialization_of_moe: bool: initialization of moe needs to
                disable some dynamic part's this boolean variable will
                turn them off.
            rope_scaling: Dict[str, Union[str, float]]: rope_scaling for
                rope

        Returns:
            A tuple of the following:
        """
        self.attention_dropout = attention_dropout
        self.attention_bias = attention_bias
        self.rope_scaling = rope_scaling
        self.number_rep_kv = number_rep_kv
        self.gradient_checkpointing = gradient_checkpointing
        self.use_scan_mlp = use_scan_mlp
        self.scan_mlp_chunk_size = scan_mlp_chunk_size
        self.bits = bits
        self.initialization_of_moe = initialization_of_moe

    @staticmethod
    def get_weight_decay_exclusions():
        return tuple()

    @staticmethod
    def rng_keys():
        return 'params', 'dropout', 'fcm'
