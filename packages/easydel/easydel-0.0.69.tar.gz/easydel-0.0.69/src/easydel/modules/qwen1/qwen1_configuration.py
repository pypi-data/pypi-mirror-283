from typing import Optional, Mapping
from jax.sharding import PartitionSpec

from easydel.modules.easydel_modelling_utils import EasyDeLPretrainedConfig


class Qwen1Config(EasyDeLPretrainedConfig):
    model_type: str = "qwen"

    def __init__(
            self,
            vocab_size=151936,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
            emb_dropout_prob=0.0,
            attn_dropout_prob=0.0,
            layer_norm_epsilon=1e-6,
            initializer_range=0.02,
            seq_length=8192,
            scale_attn_weights=True,
            use_cache=True,
            kv_channels=128,
            rotary_pct=1.0,
            rotary_emb_base=10000,
            use_dynamic_ntk=True,
            use_logn_attn=True,
            intermediate_size=22016,
            no_bias=True,
            tie_word_embeddings=False,
            softmax_in_fp32=False,
            gradient_checkpointing: str = "nothing_saveable",
            use_scan_mlp: bool = False,
            scan_mlp_chunk_size: int = 1024,
            bits: Optional[int] = None,
            scan_layers: bool = True,
            init_rope_cache_auto: bool = False,
            **kwargs,
    ):
        self.vocab_size = vocab_size
        self.seq_length = seq_length
        self.hidden_size = hidden_size
        self.intermediate_size = intermediate_size
        self.scale_attn_weights = scale_attn_weights
        self.no_bias = no_bias
        self.kv_channels = kv_channels
        self.use_dynamic_ntk = use_dynamic_ntk
        self.use_logn_attn = use_logn_attn
        self.rotary_emb_base = rotary_emb_base
        self.rotary_pct = rotary_pct
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.layer_norm_epsilon = layer_norm_epsilon
        self.softmax_in_fp32 = softmax_in_fp32
        self.initializer_range = initializer_range
        self.use_cache = use_cache
        self.scan_layers = scan_layers
        self.emb_dropout_prob = emb_dropout_prob
        self.attn_dropout_prob = attn_dropout_prob
        self.init_rope_cache_auto = init_rope_cache_auto
        self.tie_word_embeddings = tie_word_embeddings
        self.gradient_checkpointing = gradient_checkpointing
        self.use_scan_mlp = use_scan_mlp
        self.scan_mlp_chunk_size = scan_mlp_chunk_size
        self.bits = bits
        super().__init__(
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
            2) A PartitionScheme object that defines how those parameters should be partitioned across devices.

        Args:
            fully_sharded_data_parallel: bool: Determine whether to
                partition the model fully or not

        Returns:
            A list of tuples
        """
        return (

            ("model/wte/embedding", PartitionSpec("tp", ("fsdp", "sp"))),

            ("self_attn/c_attn/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
            ("self_attn/c_proj/kernel", PartitionSpec("tp", ("fsdp", "sp"))),

            ("mlp/w1/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
            ("mlp/w2/kernel", PartitionSpec(("fsdp", "sp")), "tp"),
            ("mlp/c_proj/kernel", PartitionSpec("tp", ("fsdp", "sp"))),

            ("ln_1/kernel", PartitionSpec(None)),
            ("ln_2/kernel", PartitionSpec(None)),

            ("model/ln_f/kernel", PartitionSpec(None)),
            ("lm_head/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
            (".*", PartitionSpec(None)),
        ) if not fully_sharded_data_parallel else (

            ("model/wte/embedding", PartitionSpec(("fsdp", "sp"))),

            ("self_attn/(q_proj|k_proj|v_proj)/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
            ("self_attn/o_proj/kernel", PartitionSpec("tp", ("sp", "fsdp"))),

            ("mlp/w1/kernel", PartitionSpec(("fsdp", "sp"))),
            ("mlp/w2/kernel", PartitionSpec(("fsdp", "sp"))),
            ("mlp/c_proj/kernel", PartitionSpec(("fsdp", "sp"))),

            ("ln_1/kernel", PartitionSpec(None)),
            ("ln_2/kernel", PartitionSpec(None)),

            ("model/ln_f/kernel", PartitionSpec(None)),
            ("lm_head/kernel", PartitionSpec(("fsdp", "sp"))),
            (".*", PartitionSpec(None)),

        )

    def add_jax_args(
            self,
            gradient_checkpointing: str = "nothing_saveable",
            use_scan_mlp: bool = False,
            scan_mlp_chunk_size: int = 1024,
            bits: Optional[int] = None,
            scan_layers: bool = True,
            init_rope_cache_auto: bool = False,
            **kwargs,
    ):
        """The add_jax_args function adds the following arguments to the Transformer class:

        Args:
            self: Refer to the current object
            gradient_checkpointing: str: Control the amount of memory
                used by jax
            use_scan_mlp: bool: Determine whether to use the scan_mlp
                function or not
            scan_mlp_chunk_size: int: Set the chunk size for scan_mlp
            init_rope_cache_auto: bool: Whether to use the
                rope_cache_auto in model
            bits: Optional[int]: Determine the number of bits used in
                the quantization
            scan_layers: bool: Determine whether to use scan layers or
                not

        Returns:
            The following:
        """
        self.scan_layers = scan_layers
        self.gradient_checkpointing = gradient_checkpointing
        self.use_scan_mlp = use_scan_mlp
        self.scan_mlp_chunk_size = scan_mlp_chunk_size
        self.bits = bits
        self.init_rope_cache_auto = init_rope_cache_auto

    @staticmethod
    def get_weight_decay_exclusions():
        return tuple()

    @staticmethod
    def rng_keys():
        return "params", "dropout", "fcm"
