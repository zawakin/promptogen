import json
from abc import ABC, abstractmethod
from typing import Any

from .format_utils import with_code_block

"""The type of the input value."""
InputValue = dict[str, Any]


class InputFormatter(ABC):
    @abstractmethod
    def name(self) -> str:
        """The name of the input format."""
        pass

    @abstractmethod
    def format(self, input: InputValue) -> str:
        """Format the input value into a string."""
        pass


class JsonInputFormatter(InputFormatter):
    def name(self) -> str:
        return "json"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be a dict, got {type(input).__name__}.")

        return with_code_block("json", json.dumps(input, ensure_ascii=False))
