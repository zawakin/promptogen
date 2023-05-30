import json
from abc import ABC, abstractmethod
from typing import Any

from .format_utils import remove_code_block, with_code_block

"""The type of the output value.""" ""
OutputValue = dict[str, Any]


class OutputFormatter(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def constraints(self) -> str:
        pass

    @abstractmethod
    def format(self, output: OutputValue) -> str:
        pass

    @abstractmethod
    def parse(self, output: str) -> OutputValue:
        pass


class JsonOutputFormatter(OutputFormatter):
    """The json output formatter.

    Args:
        strict (bool, optional): Whether to check if the output starts and ends with ```json. Defaults to True.
        indent (int | None, optional): The indent to use. Defaults to 1.
    """

    strict: bool
    indent: int | None

    def __init__(self, strict: bool = True, indent: int | None = 1):
        self.strict = strict
        self.indent = indent

    def name(self) -> str:
        return "json"

    def constraints(self) -> str:
        """The constraints for the json output formatter."""

        # add constraints message for deep-nested json to be parsed correctly
        # be careful with the order of brackets

        return "Be careful with the order of brackets in the json."

    def format(self, output: OutputValue) -> str:
        """Format the output value into a string.

        Args:
            output (OutputValue): The output value.

        Raises:
            TypeError: If the output is not a dict.

        Returns:
            str: The formatted output.
        """
        if not isinstance(output, dict):
            raise TypeError(f"Expected output to be a dict, got {type(output).__name__}; " "output: {output}")

        return with_code_block("json", json.dumps(output, ensure_ascii=False, indent=self.indent))

    def parse(self, output: str) -> OutputValue:
        output = output.strip()

        if self.strict:
            if not output.startswith("```json"):
                raise ValueError("Expected output to start with ```json.")
            if not output.endswith("```"):
                raise ValueError("Expected output to end with ```.")

        return json.loads(remove_code_block("json", output))


class CodeOutputFormatter(OutputFormatter):
    language: str
    output_key: str

    def __init__(self, language: str, output_key: str = "code"):
        self.language = language
        self.output_key = output_key

    def name(self) -> str:
        return "code"

    def constraints(self) -> str:
        return ""

    def format(self, output: OutputValue) -> str:
        """Format the output value into a string.

        Args:
            output (OutputValue): The output value. Must be a dict with the key `self.output_key` (default: `code`).
        """
        if not isinstance(output, dict):
            raise TypeError(f"Expected output to be a dict, got {type(output).__name__}; " "output: {output}")
        if self.output_key not in output:
            raise ValueError(f"Expected output to have key {self.output_key}.")

        return with_code_block(self.language, output[self.output_key])

    def parse(self, output: str) -> OutputValue:
        result = remove_code_block(self.language, output)
        return {self.output_key: result}


class TextOutputFormatter(OutputFormatter):
    output_key: str

    def __init__(self, output_key: str = "text"):
        self.output_key = output_key

    def name(self) -> str:
        return "text"

    def constraints(self) -> str:
        return ""

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, dict):
            raise TypeError(f"Expected output to be a dict, got {type(output).__name__}; " "output: {output}")
        if self.output_key not in output:
            raise ValueError(f"Expected output to have key {self.output_key}.")
        if not isinstance(output[self.output_key], str):
            raise TypeError(f"Expected output[{self.output_key}] to be a str, got {type(output[self.output_key])}.")
        return output[self.output_key]

    def parse(self, output: str) -> OutputValue:
        return {self.output_key: output}


class KeyValueOutputFormatter(OutputFormatter):
    def name(self) -> str:
        return "key_value"

    def constraints(self) -> str:
        return ""

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, dict):
            raise TypeError(f"Expected output to be a dict, got {type(output).__name__}; " "output: {output}")

        s = ""
        for key, value in output.items():
            # only support primitive types
            if not isinstance(value, (str, int, float, bool)):
                raise TypeError(f"Expected output[{key}] to be a primitive type, got {type(value).__name__}.")
            s += f"{key}: {value}\n"

        return s

    def parse(self, output: str) -> OutputValue:
        if not isinstance(output, str):
            raise TypeError(f"Expected formatted_str to be a str, got {type(output).__name__}.")

        lines = output.split("\n")
        result: dict[str, str | int | float | bool] = {}
        for line in lines:
            if not line:
                continue
            split_line = line.split(": ", 1)
            if len(split_line) != 2:
                raise ValueError(f"Invalid line format: {line}. Expected format 'key: value.'")

            key, value = split_line
            # Parse value to the appropriate primitive type
            if value.isdigit():
                result[key] = int(value)
            elif value.replace(".", "", 1).isdigit():
                # Only support floats with one decimal point not "1.e-10"
                f = float(value)
                result[key] = f
            elif value.lower() in ["true", "false"]:
                b = value.lower() == "true"
                result[key] = b
            else:
                result[key] = str(value)

        return result
