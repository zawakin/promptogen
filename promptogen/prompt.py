from typing import Any

from pydantic import BaseModel, validator, root_validator

from .dataclass import DataClass
from .input import InputValue
from .output import OutputValue


class ParameterInfo(BaseModel):
    """Information about a parameter.

    Attributes:
        name: The name of the parameter.
        description: A description of the parameter.
    """
    name: str
    description: str


class Example(BaseModel):
    """An few-shot example of a prompt.

    Attributes:
        input: The input to the prompt.
        output: The output of the prompt.
    """
    input: InputValue
    output: OutputValue


class Prompt(BaseModel):
    """A prompt.

    Attributes:
        name: The name of the prompt.
        description: A description of the prompt.
        input_parameters: The parameter information of the prompt's input.
        output_parameters: The parameter information of the prompt's output.
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
        if not isinstance(d, dict):
            raise TypeError(f"Expected dict, got {type(d)}")
        return cls.parse_obj(d)

    @classmethod
    def from_json(cls, json_str: str) -> "Prompt":
        return cls.parse_raw(json_str)

    @root_validator
    def validate_template(cls, values):
        template = values.get("template")
        input_parameters = values.get("input_parameters")
        output_parameters = values.get("output_parameters")

        if template is None or input_parameters is None or output_parameters is None:
            raise ValueError(
                "Template, input parameters, and output parameters must be provided")

        if template.input.keys() != {param.name for param in input_parameters}:
            raise ValueError(
                f"Template input keys do not match input parameters: {template.input.keys()} vs {input_parameters}")
        if template.output.keys() != {param.name for param in output_parameters}:
            raise ValueError(
                f"Template output keys do not match output parameters: {template.output.keys()} vs {output_parameters}")

        return values

    @root_validator
    def validate_examples(cls, values):
        examples = values.get("examples")
        input_parameters = values.get("input_parameters")
        output_parameters = values.get("output_parameters")

        if examples is None or input_parameters is None or output_parameters is None:
            raise ValueError(
                "Examples, input parameters, and output parameters must be provided")

        for example in examples:
            if example.input.keys() != {param.name for param in input_parameters}:
                raise ValueError(
                    f"Example input keys do not match input parameters: {example.input.keys()} vs {input_parameters}")
            if example.output.keys() != {param.name for param in output_parameters}:
                raise ValueError(
                    f"Example output keys do not match output parameters: {example.output.keys()} vs {output_parameters}")

        return values

    def __repr__(self) -> str:
        return self.json(indent=4)
