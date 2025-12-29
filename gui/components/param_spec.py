# gui/components/param_spec.py
from dataclasses import dataclass
from typing import Type, Any


@dataclass(frozen=True)
class ParamSpec:
    name: str
    type: Type
    optional: bool = False
    default: Any | None = None
