from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from ast import literal_eval
from pprint import pformat
from typing import Any, Dict, List, Tuple

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
    def parse(self, output_keys: List[Tuple[str, type]], output: str) -> OutputValue:
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

    def parse(self, output_keys: List[Tuple[str, type]], output: str) -> OutputValue:
        output = output.strip()

        if self.strict:
            if not output.startswith("```json"):
                raise ValueError("Expected output to start with ```json.")
            if not output.endswith("```"):
                raise ValueError("Expected output to end with ```.")

        resp = json.loads(remove_code_block("json", output))

        for key, _ in output_keys:
            if key not in resp:
                raise ValueError(f"Expected output to have key {key}.")

        return OutputValue.from_dict(resp)


class KeyValueOutputFormatter(OutputFormatter):
    def description(self) -> str:
        # return ""
        return "You should follow 'Template' format. The format is 'key: value'."

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, OutputValue):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(output).__name__}.")

        s = ""
        for key, value in output.dict().items():
            if isinstance(value, str):
                s += f'{key}: """{value}"""\n'
            else:
                pretty_value = pformat(value, indent=2, sort_dicts=False, width=160)
                s += f"{key}: {pretty_value}\n"

        return s.strip()

    def parse(self, output_keys: List[Tuple[str, type]], output: str) -> OutputValue:
        if not isinstance(output, str):
            raise TypeError(f"Expected formatted_str to be a str, got {type(output).__name__}.")

        for key, _ in output_keys:
            if key not in output:
                raise ValueError(f"Expected output to have key {key}.")

        if len(output_keys) == 0:
            raise ValueError("Expected output_keys to have at least one key.")

        result = {}

        for idx, (key, key_type) in enumerate(output_keys):
            next_key = output_keys[idx + 1][0] if idx + 1 < len(output_keys) else None
            if next_key:
                pattern = re.compile(f"{key}:.*?(?={next_key}:)", re.MULTILINE | re.DOTALL)
            else:
                pattern = re.compile(f"{key}:.*", re.MULTILINE | re.DOTALL)
            value = re.search(pattern, output)
            if value is None:
                raise ValueError(f"Expected output to have key {key}.")

            m: re.Match[str] = value
            s = m.group().replace(f"{key}:", "").strip()

            if key_type == str:
                extracted_str, found = extract_string(s)
                if found:
                    result[key] = extracted_str
                    continue
                # The value will be a raw string without quotes.
                result[key] = s

            result[key] = literal_eval(s)

        return OutputValue.from_dict(result)


def extract_string(s: str) -> Tuple[str, bool]:
    # patternsとそれに対応するフラグをリストで定義します
    patterns_flags = [(r'"""(.*?)"""', re.DOTALL), (r'"(.*?)"', 0), (r"'(.*?)'", 0)]

    for pattern, flags in patterns_flags:
        match = re.search(pattern, s, flags)
        if match:
            return match.group(1), True
    return "", False


class TextOutputFormatter(OutputFormatter):
    output_key: str

    def __init__(self, output_key: str):
        self.output_key = output_key

    def description(self) -> str:
        return ""

    def format(self, output: OutputValue) -> str:
        return output[self.output_key]

    def parse(self, _: List[Tuple[str, type]], output: str) -> OutputValue:
        return OutputValue.from_dict({self.output_key: output})
