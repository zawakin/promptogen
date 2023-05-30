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


class CodeInputFormatter(InputFormatter):
    language: str
    input_key: str

    def __init__(self, language: str, input_key: str = "code"):
        self.language = language
        self.input_key = input_key

    def name(self) -> str:
        return "code"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be a dict, got {type(input).__name__}.")

        return with_code_block(self.language, input[self.input_key])

class TextInputFormatter(InputFormatter):
    input_key: str

    def __init__(self, input_key: str = "text"):
        self.input_key = input_key

    def name(self) -> str:
        return "raw-text"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be a dict, got {type(input).__name__}.")

        return input[self.input_key]

class ListInputFormatter(InputFormatter):
    def name(self) -> str:
        return "list"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be a dict, got {type(input).__name__}.")

        s = ""
        for key, value in input.items():
            s += f"{key}: {value}\n"

        return s
