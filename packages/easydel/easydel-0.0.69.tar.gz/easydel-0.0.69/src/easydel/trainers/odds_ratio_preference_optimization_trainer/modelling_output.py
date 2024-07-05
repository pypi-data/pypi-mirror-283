from dataclasses import dataclass
import jax
from typing import Any, Optional, Callable, Mapping
from easydel.etils.easystate import EasyDeLState


@dataclass
class ORPOTrainerOutput:
    state: EasyDeLState
    mesh: Optional[jax.sharding.Mesh]
    checkpoint_manager: Any
    gather_fns: Optional[Any | Mapping[str, Callable] | dict[str, Callable]] = None
    shard_fns: Optional[Any | Mapping[str, Callable] | dict[str,Callable]] = None
    last_save_file_name: Optional[str] = None
    checkpoint_path: Optional[str] = None
