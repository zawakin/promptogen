from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel

from promptgen.dataclass import DictLike

from .format_utils import remove_code_block, with_code_block


class OutputValue(DictLike):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OutputValue":
        if not isinstance(data, dict):
            raise TypeError("OutputValue.from_dict() only accepts dict")
        return cls.parse_obj(data)

    @classmethod
    def from_dataclass(cls, data: BaseModel) -> "OutputValue":
        if not isinstance(data, BaseModel):
            raise TypeError("OutputValue.from_BaseModel() only accepts BaseModel")
        return cls.parse_obj(data)


class OutputFormatter(ABC):
    @abstractmethod
    def description(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def format(self, output: OutputValue) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def parse(self, output: str) -> OutputValue:
        pass  # pragma: no cover


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
        if not isinstance(output, OutputValue):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(output).__name__}.")

        return with_code_block("json", output.json(ensure_ascii=False, indent=self.indent))

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

    def description(self) -> str:
        return f"""Output a code-block in {self.language} without outputting any other strings."""

    def format(self, output: OutputValue) -> str:
        """Format the output value into a string.

        Args:
            output (OutputValue): The output value. Must be a dict with the key `self.output_key` (default: `code`).
        """
        if not isinstance(output, OutputValue):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(output).__name__}.")
        if self.output_key not in output.dict():
            raise ValueError(f"Expected output to have key {self.output_key}.")

        return with_code_block(self.language, output[self.output_key])

    def parse(self, output: str) -> OutputValue:
        result = remove_code_block(self.language, output)
        return OutputValue.from_dict({self.output_key: result})


class TextOutputFormatter(OutputFormatter):
    output_key: str

    def __init__(self, output_key: str = "text"):
        self.output_key = output_key

    def description(self) -> str:
        return ""

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, OutputValue):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(output).__name__}.")
        if self.output_key not in output.dict():
            raise ValueError(f"Expected output to have key {self.output_key}.")
        print(output[self.output_key], type(output[self.output_key]))
        if not isinstance(output[self.output_key], str):
            raise TypeError(f"Expected output[{self.output_key}] to be a str, got {type(output[self.output_key])}.")
        return output[self.output_key]

    def parse(self, output: str) -> OutputValue:
        return OutputValue.from_dict({self.output_key: output})


class KeyValueOutputFormatter(OutputFormatter):
    def description(self) -> str:
        return "You should follow 'Template' format. The format is 'key: value'."

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, OutputValue):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(output).__name__}.")

        s = ""
        for key, value in output.dict().items():
            if isinstance(value, str):
                value = f"'{value}'"
            s += f"{key}: {value}\n"

        return s.strip()

    def parse(self, output: str) -> OutputValue:
        if not isinstance(output, str):
            raise TypeError(f"Expected formatted_str to be a str, got {type(output).__name__}.")

        lines = output.split("\n")
        result: Dict[str, Any] = {}
        from ast import literal_eval

        for line in lines:
            split_line = line.split(": ", 1)
            if len(split_line) != 2:
                raise ValueError(f"Invalid line format: {line}. Expected format 'key: value.'")

            val = split_line[1]
            obj = literal_eval(val)
            result[split_line[0]] = obj

        return OutputValue.from_dict(result)
