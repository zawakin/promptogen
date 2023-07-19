from typing import List, Tuple

from promptgen.model.value_formatter import Value, ValueFormatter


class TextValueFormatter(ValueFormatter):
    key: str

    def __init__(self, output_key: str):
        self.key = output_key

    def description(self) -> str:
        return ""

    def format(self, output: Value) -> str:
        return output[self.key]

    def parse(self, _: List[Tuple[str, type]], output: str) -> Value:
        return {self.key: output}
