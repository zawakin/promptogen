from typing import List, Tuple

from promptgen.model.output_formatter import OutputFormatter, OutputValue


class TextOutputFormatter(OutputFormatter):
    output_key: str

    def __init__(self, output_key: str):
        self.output_key = output_key

    def description(self) -> str:
        return ""

    def format(self, output: OutputValue) -> str:
        return output[self.output_key]

    def parse(self, _: List[Tuple[str, type]], output: str) -> OutputValue:
        return {self.output_key: output}
