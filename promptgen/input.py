from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from promptgen.dataclass import DataClass, DictLike

from .format_utils import with_code_block


class InputValue(DictLike):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InputValue":
        if not isinstance(data, dict):
            raise TypeError("InputValue.from_dict() only accepts dict")
        return cls.parse_obj(data)

    @classmethod
    def from_dataclass(cls, data: DataClass) -> "InputValue":
        if not isinstance(data, DataClass):
            raise TypeError("InputValue.from_dataclass() only accepts DataClass")
        return cls.parse_obj(data)


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
        if not isinstance(input, InputValue):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        return with_code_block("json", input.json(ensure_ascii=False))


class CodeInputFormatter(InputFormatter):
    language: str
    input_key: str

    def __init__(self, language: str, input_key: str = "code"):
        self.language = language
        self.input_key = input_key

    def name(self) -> str:
        return "code"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, InputValue):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        return with_code_block(self.language, input[self.input_key])


class TextInputFormatter(InputFormatter):
    input_key: str

    def __init__(self, input_key: str = "text"):
        self.input_key = input_key

    def name(self) -> str:
        return "raw-text"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, InputValue):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        return input[self.input_key]


class KeyValueInputFormatter(InputFormatter):
    def name(self) -> str:
        return "key_value"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, InputValue):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        s = ""
        for key, value in input.dict().items():
            if isinstance(value, str):
                s += f"{key}: '{value}'\n"
            else:
                s += f"{key}: {value}\n"

        return s.strip()
