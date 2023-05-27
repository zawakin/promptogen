import json
from abc import ABC, abstractmethod
from typing import Any

from .format_utils import remove_code_block, with_code_block

"""The type of the output value.""" ""
OutputValue = str | dict[str, Any]


class OutputFormatter(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def format(self, output: OutputValue) -> str:
        pass

    @abstractmethod
    def parse(self, output: str) -> OutputValue:
        pass


class JsonOutputFormatter(OutputFormatter):
    def __init__(self, strict: bool = True):
        self.strict = strict

    def name(self) -> str:
        return "json"

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, dict):
            raise TypeError(
                f"Expected output to be a dict, got {type(output).__name__}; "
                "output: {output}"
            )

        return with_code_block("json", json.dumps(output, ensure_ascii=False))

    def parse(self, output: str) -> OutputValue:
        output = output.strip()

        if self.strict:
            if not output.startswith("```json"):
                raise ValueError("Expected output to start with ```json.")
            if not output.endswith("```"):
                raise ValueError("Expected output to end with ```.")

        return json.loads(remove_code_block("json", output))


class RawStringOutputFormatter(OutputFormatter):
    def name(self) -> str:
        return "raw-string"

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, str):
            raise ValueError("RawStringOutputFormatter can only format strings.")

        return output

    def parse(self, output: str) -> OutputValue:
        return output
