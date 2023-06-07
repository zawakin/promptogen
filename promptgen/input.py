from __future__ import annotations

from abc import ABC, abstractmethod
from pprint import pformat
from typing import Any, Dict

from pydantic import BaseModel

from promptgen.dataclass import DictLike

from .format_utils import with_code_block


class InputValue(DictLike):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InputValue":
        if not isinstance(data, dict):
            raise TypeError("InputValue.from_dict() only accepts dict")
        return cls.parse_obj(data)

    @classmethod
    def from_dataclass(cls, data: BaseModel) -> "InputValue":
        if not isinstance(data, BaseModel):
            raise TypeError("InputValue.from_BaseModel() only accepts BaseModel")
        return cls.parse_obj(data)


class InputFormatter(ABC):
    @abstractmethod
    def format(self, input: InputValue) -> str:
        """Format the input value into a string."""
        pass  # pragma: no cover


class JsonInputFormatter(InputFormatter):
    def format(self, input: InputValue) -> str:
        if not isinstance(input, InputValue):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        return with_code_block("json", input.json(ensure_ascii=False))


class KeyValueInputFormatter(InputFormatter):
    def format(self, input: InputValue) -> str:
        if not isinstance(input, InputValue):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        s = ""
        for key, value in input.dict().items():
            if isinstance(value, str):
                s += f'{key}: """{value}"""\n'
            else:
                pretty_value = pformat(value, indent=2, sort_dicts=False, width=160)
                s += f"{key}: {pretty_value}\n"

        return s.strip()
