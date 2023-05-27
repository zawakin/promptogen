from typing import Any

from .dataclass import DataClass
from .input import InputValue
from .output import OutputValue


class ParameterInfo(DataClass):
    """Information about a parameter.

    Attributes:
        name: The name of the parameter.
        description: A description of the parameter.
    """
    name: str
    description: str


class Example(DataClass):
    """An few-shot example of a prompt.

    Attributes:
        input: The input to the prompt.
        output: The output of the prompt.
    """
    input: InputValue
    output: OutputValue


class Prompt(DataClass):
    """A prompt.

    Attributes:
        name: The name of the prompt.
        description: A description of the prompt.
        input_parameters: The parameters of the prompt's input.
        output_parameters: The parameters of the prompt's output.
        template: An example of the prompt.
        examples: A list of examples of the prompt.
    """

    name: str
    description: str
    input_parameters: list[ParameterInfo]
    output_parameters: list[ParameterInfo]
    template: Example
    examples: list[Example]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Prompt":
        return cls(**d)
