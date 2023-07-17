from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pprint import pformat
from typing import Any, Callable, Dict

from typing_extensions import TypeAlias

InputValue: TypeAlias = Dict[str, Any]


class InputFormatter(ABC):
    @abstractmethod
    def format(self, input: InputValue) -> str:
        """Format the input value into a string."""
        pass  # pragma: no cover
