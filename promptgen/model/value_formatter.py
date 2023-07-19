from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from typing_extensions import TypeAlias

Value: TypeAlias = Dict[str, Any]


class ValueFormatter(ABC):
    @abstractmethod
    def description(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def format(self, value: Value) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def parse(self, key_types: List[Tuple[str, type]], s: str) -> Value:
        pass  # pragma: no cover
