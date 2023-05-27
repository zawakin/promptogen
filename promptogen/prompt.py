from typing import Any

from pydantic import BaseModel

from .input import InputFormatter, InputValue
from .output import OutputFormatter, OutputValue

class ParameterInfo(BaseModel):
    name: str
    description: str


class Example(BaseModel):
    input: InputValue
    output: OutputValue

    def format(self, inputFormatter: InputFormatter, outputFormatter: OutputFormatter) -> str:
        formatted_input = inputFormatter.format(self.input)
        formatted_output = outputFormatter.format(self.output)
        return f"Input:\n{formatted_input}\nOutput:\n{formatted_output}"


class Prompt(BaseModel):
    name: str
    description: str
    input_parameters: list[ParameterInfo]
    output_parameters: list[ParameterInfo]
    template: Example
    examples: list[Example]
    
    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Prompt":
        return cls(**d)

