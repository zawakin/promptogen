
from abc import ABC, abstractmethod
import json
from typing import Any

from .format_utils import with_code_block

InputValue = dict[str, Any]


class InputFormatter(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def format(self, input: InputValue) -> str:
        pass

class JsonInputFormatter(InputFormatter):
    def name(self) -> str:
        return "json"

    def format(self, input: InputValue) -> str:
        return with_code_block("json", json.dumps(input, ensure_ascii=False))

