from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pprint import pformat
from typing import Any, Dict

from typing_extensions import TypeAlias

from .format_utils import with_code_block

InputValue: TypeAlias = Dict[str, Any]


class InputFormatter(ABC):
    @abstractmethod
    def format(self, input: InputValue) -> str:
        """Format the input value into a string."""
        pass  # pragma: no cover


class JsonInputFormatter(InputFormatter):
    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        return with_code_block("json", json.dumps(input, ensure_ascii=False))


class KeyValueInputFormatter(InputFormatter):
    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        s = ""
        for key, value in input.items():
            if isinstance(value, str):
                s += f'{key}: """{value}"""\n'
            else:
                pretty_value = pformat(value, indent=2, sort_dicts=False, width=160)
                s += f"{key}: {pretty_value}\n"

        return s.strip()
