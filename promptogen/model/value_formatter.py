from __future__ import annotations

import typing
from typing import Any, Dict, List, Tuple

from typing_extensions import TypeAlias

Value: TypeAlias = Dict[str, Any]


class ValueFormatter(typing.Protocol):
    def description(self) -> str: ...

    def format(self, value: Value) -> str: ...

    def parse(self, key_types: List[Tuple[str, type]], output: str) -> Value: ...
