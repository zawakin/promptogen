
from abc import ABC, abstractmethod
import json
from typing import Any

from .format_utils import remove_code_block, with_code_block

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
    def name(self) -> str:
        return "json"

    def format(self, output: OutputValue) -> str:
        return with_code_block("json", json.dumps(output, ensure_ascii=False))

    def parse(self, output: str) -> OutputValue:
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
