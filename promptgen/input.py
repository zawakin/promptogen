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


class KeyValueInputFormatter(InputFormatter):
    def name(self) -> str:
        return "key-value"

    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be a dict, got {type(input).__name__}.")

        result = ""

        # int, bool, float -> use key value
        # str -> use multiline string using ("""<content>""")
        # dict -> use json
        # list -> use array like [1, 2, 3]

        for key, value in input.items():
            if isinstance(value, int) or isinstance(value, bool) or isinstance(value, float):
                result += f"{key}: {value}\n"
            elif isinstance(value, str):
                result += f"{key}: \"\"\"{value}\"\"\"\n"
            elif isinstance(value, dict):
                result += f"{key}:\n{with_code_block('json', json.dumps(value, ensure_ascii=False))}\n"
            elif isinstance(value, list):
                result += f"{key}: {value}\n"
            else:
                raise TypeError(f"Expected value to be a int, bool, float, str, dict or list, got {type(value).__name__}.")

        return result

