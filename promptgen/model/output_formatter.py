from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from ast import literal_eval
from pprint import pformat
from typing import Any, Callable, Dict, List, Tuple

from typing_extensions import TypeAlias

OutputValue: TypeAlias = Dict[str, Any]


class OutputFormatter(ABC):
    @abstractmethod
    def description(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def format(self, output: OutputValue) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def parse(self, output_keys: List[Tuple[str, type]], output: str) -> OutputValue:
        pass  # pragma: no cover
