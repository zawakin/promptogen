from __future__ import annotations

from typing import Any, Dict, List, Tuple

from pydantic import model_validator

from .dataclass import DataClass
from .input_formatter import InputValue
from .output_formatter import OutputValue


class ParameterInfo(DataClass):
    """Information about a parameter.

    Attributes:
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

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Example":
        """Create an example from a dictionary.

        Args:
            d: A dictionary containing the example's information.

        Returns:
            An example.

        Raises:
            TypeError: If the dictionary is not a dictionary.
            ValueError: If the dictionary does not contain the required keys.
        """
        if not isinstance(d, dict):
            raise TypeError(f"Expected dict, got {type(d)}")
        return cls.model_validate(d)


class Prompt(DataClass):
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
    input_parameters: List[ParameterInfo]
    output_parameters: List[ParameterInfo]
    template: Example
    examples: List[Example]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Prompt":
        """Create a prompt from a dictionary.

        Args:
            d: A dictionary containing the prompt's information.

        Returns:
            A prompt.

        Raises:
            TypeError: If the dictionary is not a dictionary.
            ValueError: If the dictionary does not contain the required keys.
        """
        if not isinstance(d, dict):
            raise TypeError(f"Expected dict, got {type(d)}")
        return cls.model_validate(d)

    @classmethod
    def from_json_string(cls, json_string: str) -> "Prompt":
        """Create a prompt from a JSON string.

        Args:
            json_string: A JSON string containing the prompt's information.

        Returns:
            A prompt.

        Raises:
            TypeError: If the JSON string is not a string.
            ValueError: If the JSON string is not valid JSON.
        """
        return cls.model_validate_json(json_string)

    @classmethod
    def from_json_file(cls, filename: str) -> "Prompt":
        """Create a prompt from a JSON file.

        Args:
            filename: The name of the JSON file containing the prompt's information.

        Returns:
            A prompt.

        Raises:
            TypeError: If the filename is not a string.
            ValueError: If the file does not contain valid JSON.
        """
        with open(filename, "r") as f:
            return cls.model_validate_json(f.read())

    def to_json_file(self, filename: str, indent=4) -> None:
        with open(filename, "w") as f:
            f.write(self.model_dump_json(indent=indent))

    @model_validator(mode="after")
    def validate_template(self):
        input_parameters = self.input_parameters
        output_parameters = self.output_parameters
        template = self.template
        examples = self.examples

        input_parameter_keys = {parameter.name for parameter in input_parameters}
        output_parameter_keys = {parameter.name for parameter in output_parameters}
        if template.input.keys() != input_parameter_keys:
            raise ValueError(
                f"Template input keys do not match input parameters: " f"{template.input} vs {input_parameters}"
            )
        if template.output.keys() != output_parameter_keys:
            raise ValueError(
                f"Template output keys do not match output parameters: "
                f"{template.output.keys()} vs {output_parameters}"
            )

        for example in examples:
            if example.input.keys() != input_parameter_keys:
                raise ValueError(
                    f"Example input keys do not match input parameters: " f"{example.input} vs {input_parameters}"
                )
            if example.output.keys() != output_parameter_keys:
                raise ValueError(
                    f"Example output keys do not match output parameters: " f"{example.output} vs {output_parameters}"
                )

        return self

    def with_examples(self, examples: List[Example]) -> "Prompt":
        """Set the examples of the prompt.

        Args:
            examples: The examples to set.

        Returns:
            A copy of the prompt with the examples set.
        """
        return self.model_copy(deep=True, update={"examples": examples})

    def rename_input_parameter(self, old_name: str, new_name: str) -> "Prompt":
        """Rename an input parameter.

        Args:
            old_name: The old name of the input parameter.
            new_name: The new name of the input parameter.

        Returns:
            A copy of the prompt with the input parameter renamed.
        """
        input_parameters = [param.model_copy(deep=True) for param in self.input_parameters]
        # find the parameter
        found = False
        index = -1
        for i, parameter in enumerate(input_parameters):
            if parameter.name == old_name:
                found = True
                index = i
                break
        if not found:
            raise ValueError(f"Could not find input parameter with name {old_name}")
        input_parameters[index].name = new_name

        # rename in template
        template = self.template.model_copy(deep=True)
        template.input[new_name] = template.input.pop(old_name)

        # rename in examples
        examples = []
        for example in self.examples:
            example = example.model_copy(deep=True)
            example.input[new_name] = example.input.pop(old_name)
            examples.append(example)

        return self.model_copy(
            deep=True,
            update={
                "input_parameters": input_parameters,
                "template": template,
                "examples": examples,
            },
        )

    def rename_output_parameter(self, old_name: str, new_name: str) -> "Prompt":
        """Rename an output parameter.

        Args:
            old_name: The old name of the output parameter.
            new_name: The new name of the output parameter.

        Returns:
            A copy of the prompt with the output parameter renamed.
        """
        output_parameters = [param.model_copy(deep=True) for param in self.output_parameters]

        # find the parameter
        found = False
        index = -1
        for i, parameter in enumerate(output_parameters):
            if parameter.name == old_name:
                found = True
                index = i
                break
        if not found:
            raise ValueError(f"Could not find output parameter with name {old_name}")
        output_parameters[index].name = new_name

        # rename in template
        template = self.template.model_copy(deep=True)
        template.output[new_name] = template.output.pop(old_name)

        # rename in examples
        examples = []
        for example in self.examples:
            example = example.model_copy(deep=True)
            example.output[new_name] = example.output.pop(old_name)
            examples.append(example)

        return self.model_copy(
            deep=True,
            update={
                "output_parameters": output_parameters,
                "template": template,
                "examples": examples,
            },
        )

    def get_output_keys(self) -> List[Tuple[str, type]]:
        """Get the output keys of the prompt.

        Returns:
            The output keys of the prompt.
        """
        # return [param.name for param in self.output_parameters]
        return [(param.name, type(self.template.output[param.name])) for param in self.output_parameters]

    def __repr__(self) -> str:
        input_parameters = "\n".join(
            [
                f"    - {param.name} ({type(self.template.input[param.name]).__name__}): {param.description}"
                for param in self.input_parameters
            ]
        )
        output_parameters = "\n".join(
            [
                f"    - {param.name} ({type(self.template.output[param.name]).__name__}): {param.description}"
                for param in self.output_parameters
            ]
        )
        s = f"""Prompt: {self.name}

{self.description}

Input Parameters:
{input_parameters}

Output Parameters:
{output_parameters}
"""
        return s

    def __str__(self) -> str:
        """Return a string representation of the prompt.

        Returns:
            A string representation of the prompt.
        """
        input_str = ", ".join(
            [f"{param.name}: {type(self.template.input[param.name]).__name__}" for param in self.input_parameters]
        )
        output_str = ", ".join(
            [f"{param.name}: {type(self.template.output[param.name]).__name__}" for param in self.output_parameters]
        )
        return f"{self.name}: ({input_str}) -> ({output_str})"


def load_prompt_from_json_file(filename: str) -> Prompt:
    """Load a prompt from a JSON file.

    Args:
        filename: The name of the file to load the prompt from.

    Returns:
        The loaded prompt.
    """
    return Prompt.from_json_file(filename)


def load_prompt_from_json_string(json_str: str) -> Prompt:
    """Load a prompt from a JSON string.

    Args:
        json_str: The JSON string to load the prompt from.

    Returns:
        The loaded prompt.
    """
    return Prompt.model_validate_json(json_str)


def load_prompt_from_dict(d: Dict[str, Any]) -> Prompt:
    """Load a prompt from a dictionary.

    Args:
        d: The dictionary to load the prompt from.

    Returns:
        The loaded prompt.
    """
    return Prompt.from_dict(d)


def create_sample_prompt(suffix: str) -> Prompt:
    """Create a sample prompt.

    Args:
        suffix: The suffix to append to the prompt name.

    Returns:
        The sample prompt.
    """
    return Prompt(
        name=f"sample-{suffix}",
        description="A sample prompt.",
        input_parameters=[
            ParameterInfo(name="input1", description="The first input parameter."),
            ParameterInfo(name="input2", description="The second input parameter."),
        ],
        output_parameters=[
            ParameterInfo(name="output1", description="The first output parameter."),
            ParameterInfo(name="output2", description="The second output parameter."),
        ],
        template=Example(
            input={"input1": "Hello, world!", "input2": "Hello, world!"},
            output={"output1": "Hello, world!", "output2": "Hello, world!"},
        ),
        examples=[
            Example(
                input={"input1": "Hello, world!", "input2": "Hello, world!"},
                output={"output1": "Hello, world!", "output2": "Hello, world!"},
            ),
            Example(
                input={"input1": "Hello, world!", "input2": "Hello, world!"},
                output={"output1": "Hello, world!", "output2": "Hello, world!"},
            ),
        ],
    )