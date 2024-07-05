from typing import Dict, Optional, Union

from jax.sharding import PartitionSpec

from easydel.modules.easydel_modelling_utils import EasyDeLPretrainedConfig


class LlamaConfig(EasyDeLPretrainedConfig):
    model_type: str = "llama"

    def __init__(
        self,
        vocab_size: int = 32000,
        hidden_size: int = 4096,
        intermediate_size: int = 11008,
        num_hidden_layers: int = 32,
        num_attention_heads: int = 32,
        number_rep_kv: int = 1,
        num_key_value_heads: Optional[int] = None,
        max_position_embeddings: int = 2048,
        rms_norm_eps: float = 1e-6,
        initializer_range: float = 0.02,
        use_cache: bool = True,
        bos_token_id: int = 0,
        eos_token_id: int = 1,
        resid_pdrop: float = 0.0,
        embd_pdrop: float = 0.0,
        attention_dropout: float = 0.0,
        rope_theta: float = 10000.0,
        attention_bias: bool = False,
        tie_word_embeddings: bool = False,
        gradient_checkpointing: str = "nothing_saveable",
        fcm_min_ratio: float = -1,
        fcm_max_ratio: float = -1,
        rope_scaling: Dict[str, Union[str, float]] = None,
        scan_mlp_chunk_size: int = 1024,
        bits: Optional[int] = None,
        hidden_act: str = "silu",
        pretraining_tp: int = 1,
        mlp_bias: bool = False,
        scan_layers: bool = False,
        **kwargs,
    ):
        """The __init__ function is called when the class is instantiated.
        It sets up the attributes of an object, which are sometimes called fields or properties.
        The __init__ function can accept arguments, but self must be the first one.

        Args:
            self: Refer to the object itself
            vocab_size: int: Set the size of the vocabulary
            hidden_size: int: Set the size of the hidden layers in each
                transformer block
            intermediate_size: int: Set the size of the intermediate
                layer
            num_hidden_layers: int: Determine the number of layers in
                the transformer
            num_attention_heads: int: Determine the number of attention
                heads
            number_rep_kv: int: Set the number of times to repeat the
                key and value vectors
            num_key_value_heads: Optional[int]: Define the number of
                key-value heads
            max_position_embeddings: int: Set the maximum length of a
                sequence
            rms_norm_eps: float: Prevent division by zero in the rms
                normalization
            initializer_range: float: Initialize the weights of the
                model
            use_cache: bool: Determine whether the attention layer
                should use a cache for faster computation
            bos_token_id: int: Set the beginning of sequence token
            eos_token_id: int: Specify the end of sentence token
            resid_pdrop: float: Set the dropout rate for residual
                connections
            embd_pdrop: float: Dropout the embedding layer
            attention_dropout: float: Dropout the attention weights
            tie_word_embeddings: bool: Tie the word embeddings and
                output layer weights
            gradient_checkpointing: str: Specify how to checkpoint the
                gradients
            fcm_min_ratio: float: Set the minimum ratio of the number of
                elements in a tensor to be processed by flash
            fcm_max_ratio: float: Determine the maximum ratio of
            rope_scaling: Dict[str: Define the scaling of the rope
            Union[str: Specify the type of the parameter
            float]]: Specify the type of the parameter
            shard_attention_computation: bool: when ever to use
                shard_map for attention
            bits: Optional[int]: Specify the number of bits used to
                quantize the weights
            rope_theta: float : rope_theta for compute rope
            attention_bias: bool : whenever to use attention bias or no
            hidden_act: str : hidden_act for mlp
            axis_dims: Sequence[int]: Specify the dimensions of each
                axis
            axis_names: Sequence[str]: Specify the names of the axes in
                a tensor
            scan_layers: bool: Determine whether to use the scan_layers
                or not
            **kwargs: Pass a variable number of keyword arguments to a
                function
        :param : Define the number of layers in the model

        Returns:
            Nothing
        """
        num_key_value_heads = num_key_value_heads or number_rep_kv * num_attention_heads
        self.num_key_value_heads = num_key_value_heads
        self.vocab_size = vocab_size

        self.number_rep_kv = number_rep_kv
        self.hidden_size = hidden_size
        self.initializer_range = initializer_range
        self.intermediate_size = intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.rope_theta = rope_theta
        self.attention_bias = attention_bias
        self.num_attention_heads = num_attention_heads
        self.max_position_embeddings = max_position_embeddings
        self.rms_norm_eps = rms_norm_eps
        self.use_cache = use_cache
        self.pretraining_tp = pretraining_tp
        self.resid_pdrop = resid_pdrop
        self.embd_pdrop = embd_pdrop
        self.attention_dropout = attention_dropout
        self.gradient_checkpointing = gradient_checkpointing
        self.mlp_bias = mlp_bias
        self.fcm_min_ratio = fcm_min_ratio
        self.hidden_act = hidden_act
        self.fcm_max_ratio = fcm_max_ratio
        self.rope_scaling = rope_scaling
        self.bits = bits
        self.scan_layers = scan_layers
        super().__init__(
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            tie_word_embeddings=tie_word_embeddings,
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
            (
                ("model/embed_tokens/embedding", PartitionSpec("tp", ("fsdp", "sp"))),
                (
                    "self_attn/(q_proj|k_proj|v_proj)/kernel",
                    PartitionSpec(("fsdp", "sp"), "tp"),
                ),
                ("self_attn/o_proj/kernel", PartitionSpec("tp", ("sp", "fsdp"))),
                ("mlp/gate_proj/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
                ("mlp/down_proj/kernel", PartitionSpec("tp", ("fsdp", "sp"))),
                ("mlp/up_proj/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
                ("input_layernorm/kernel", PartitionSpec(None)),
                ("post_attention_layernorm/kernel", PartitionSpec(None)),
                ("model/norm/kernel", PartitionSpec(None)),
                ("lm_head/kernel", PartitionSpec(("fsdp", "sp"), "tp")),
                (".*", PartitionSpec(None)),
            )
            if not fully_sharded_data_parallel
            else (
                ("model/embed_tokens/embedding", PartitionSpec(("fsdp", "sp"))),
                (
                    "self_attn/(q_proj|k_proj|v_proj)/kernel",
                    PartitionSpec(("fsdp", "sp"), "tp"),
                ),
                ("self_attn/o_proj/kernel", PartitionSpec("tp", ("sp", "fsdp"))),
                ("mlp/gate_proj/kernel", PartitionSpec(("fsdp", "sp"))),
                ("mlp/down_proj/kernel", PartitionSpec(("fsdp", "sp"))),
                ("mlp/up_proj/kernel", PartitionSpec(("fsdp", "sp"))),
                ("input_layernorm/kernel", PartitionSpec(None)),
                ("post_attention_layernorm/kernel", PartitionSpec(None)),
                ("model/norm/kernel", PartitionSpec(None)),
                ("lm_head/kernel", PartitionSpec(("fsdp", "sp"))),
                (".*", PartitionSpec(("fsdp", "sp"))),
            )
        )

    def add_jax_args(
        self,
        resid_pdrop: float = 0.0,
        embd_pdrop: float = 0.0,
        attention_dropout: float = 0.0,
        tie_word_embeddings: bool = False,
        gradient_checkpointing: str = "nothing_saveable",
        fcm_min_ratio: float = 0.0,
        fcm_max_ratio: float = 0.0,
        number_rep_kv: int = 1,
        bits: Optional[int] = None,
        rope_theta: float = 10000.0,
        attention_bias: bool = False,
        hidden_act: str = "silu",
        scan_layers: bool = True,
        **kwargs,
    ):
        """The add_jax_args function adds the following arguments to the Transformer class:

        Args:
            self: Refer to the current object
            resid_pdrop: float: Set the dropout rate for residual
                connections
            embd_pdrop: float: Set the probability of dropping an
                embedding
            attention_dropout: float: Set the probability of dropping
                out the attention layer
            tie_word_embeddings: bool: Tie the word embeddings to the
                decoder
            gradient_checkpointing: str: Control the amount of memory
                used by jax
            fcm_min_ratio: float: Control the minimum ratio of the
                number of chunks to be used in flash-based computation
            fcm_max_ratio: float: Set the maximum ratio of the number of
                input tokens to output tokens
            number_rep_kv: int: Determine how many times the key and
                value vectors are repeated
            bits: Optional[int]: Determine the number of bits used in
                the quantization
            rope_theta: float : rope_theta for compute rope
            attention_bias: bool : whenever to use attention bias or no
            hidden_act: str : hidden_act for mlp
            scan_layers: bool: Determine whether to use scan layers or
                not
        """
        self.scan_layers = scan_layers
        self.embd_pdrop = embd_pdrop
        self.number_rep_kv = number_rep_kv
        self.resid_pdrop = resid_pdrop
        self.rope_theta = rope_theta
        self.attention_bias = attention_bias
        self.attention_dropout = attention_dropout
        self.hidden_act = hidden_act
        self.tie_word_embeddings = tie_word_embeddings
        self.gradient_checkpointing = gradient_checkpointing
        self.fcm_min_ratio = fcm_min_ratio
        self.fcm_max_ratio = fcm_max_ratio
        self.bits = bits

    @staticmethod
    def get_weight_decay_exclusions():
        return tuple()

    @staticmethod
    def rng_keys():
        return "params", "dropout", "fcm"
