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
    def description(self) -> str:
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

    def description(self) -> str:
        """The description of the json output formatter."""

        return """Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json."""

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

    def description(self) -> str:
        return f"""Output a code-block in {self.language} without outputting any other strings."""

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

    def description(self) -> str:
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

    def description(self) -> str:
        return "You should follow 'Template' format. The format is 'key: value'."

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, dict):
            raise TypeError(f"Expected output to be a dict, got {type(output).__name__}; " "output: {output}")

        s = ""
        for key, value in output.items():
            if isinstance(value, str):
                value = f"'{value}'"
            s += f"{key}: {value}\n"

        return s.strip()

    def parse(self, output: str) -> OutputValue:
        if not isinstance(output, str):
            raise TypeError(f"Expected formatted_str to be a str, got {type(output).__name__}.")

        lines = output.split("\n")
        result: dict[str, Any] = {}
        from ast import literal_eval

        for line in lines:
            if not line:
                continue
            split_line = line.split(": ", 1)
            if len(split_line) != 2:
                raise ValueError(f"Invalid line format: {line}. Expected format 'key: value.'")

            val = split_line[1]
            obj = literal_eval(val)
            result[split_line[0]] = obj

        return result
