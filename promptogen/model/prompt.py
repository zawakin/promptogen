from __future__ import annotations

from typing import Any, Dict, List

from pydantic import model_validator

from .dataclass import DataClass
from .value_formatter import Value


class ParameterInfo(DataClass):
    """Information about a parameter.

    Attributes:
        description: A description of the parameter.
    """

    name: str
    description: str


class IOExample(DataClass):
    """An few-shot example of a prompt.

    Attributes:
        input: The input to the prompt.
        output: The output of the prompt.
    """

    input: Value
    output: Value


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
    template: IOExample
    examples: List[IOExample]

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
                f"Template input keys do not match input parameters: " f"{template.input.keys()} vs {input_parameters}"
            )
        if template.output.keys() != output_parameter_keys:
            raise ValueError(
                f"Template output keys do not match output parameters: {template.output.keys()} vs {output_parameters}"
            )

        for example in examples:
            if example.input.keys() != input_parameter_keys:
                raise ValueError(
                    f"Example input keys do not match input parameters: "
                    f"{example.input.keys()} vs {input_parameters}"
                )
            if example.output.keys() != output_parameter_keys:
                raise ValueError(
                    f"Example output keys do not match output parameters: "
                    f"{example.output.keys()} vs {output_parameters}"
                )

        return self

    def rename_input_parameter(self, old_name: str, new_name: str) -> "Prompt":
        """Rename an input parameter.

        Args:
            old_name: The old name of the input parameter.
            new_name: The new name of the input parameter.

        Returns:
            A copy of the prompt with the input parameter renamed.
        """
        input_parameters = [param.copy() for param in self.input_parameters]
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
        template = self.template.copy()
        template.input[new_name] = template.input.pop(old_name)

        # rename in examples
        examples = []
        for example in self.examples:
            example = example.copy()
            example.input[new_name] = example.input.pop(old_name)
            examples.append(example)

        return self.update(
            input_parameters=input_parameters,
            template=template,
            examples=examples,
        )

    def rename_output_parameter(self, old_name: str, new_name: str) -> "Prompt":
        """Rename an output parameter.

        Args:
            old_name: The old name of the output parameter.
            new_name: The new name of the output parameter.

        Returns:
            A copy of the prompt with the output parameter renamed.
        """
        output_parameters = [param.copy() for param in self.output_parameters]

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
        template = self.template.copy()
        template.output[new_name] = template.output.pop(old_name)

        # rename in examples
        examples = []
        for example in self.examples:
            example = example.copy()
            example.output[new_name] = example.output.pop(old_name)
            examples.append(example)

        return self.update(
            output_parameters=output_parameters,
            template=template,
            examples=examples,
        )

    def summary(self) -> str:
        def section_header(title):
            return f"\n{title}\n" + "-" * len(title)

        input_params_str = "\n".join(
            [
                f"- {param.name} ({type(self.template.input[param.name]).__name__}): {param.description}"
                for param in self.input_parameters
            ]
        )
        output_params_str = "\n".join(
            [
                f"- {param.name} ({type(self.template.output[param.name]).__name__}): {param.description}"
                for param in self.output_parameters
            ]
        )

        signature = f"{self.name}: {self.function_signature()}"
        description = f"{section_header('Description')}\n{self.description}"
        input_parameters = f"{section_header('Input Parameters')}\n{input_params_str}"
        output_parameters = f"{section_header('Output Parameters')}\n{output_params_str}"
        examples_count = f"{section_header('Examples Count')}\n{len(self.examples)}"

        return f"{signature}\n" f"{description}\n" f"{input_parameters}\n" f"{output_parameters}\n" f"{examples_count}"

    def __repr__(self) -> str:
        input_parameter_names = [param.name for param in self.input_parameters]
        output_parameter_names = [param.name for param in self.output_parameters]
        return f"{self.__class__.__name__}(name={self.name!r}, description='{self.description[:20]}...', input_parameter_names={input_parameter_names!r}, output_parameter_names={output_parameter_names!r}, examples_count={len(self.examples)})"

    def __str__(self) -> str:
        """Return a string representation of the prompt.

        Returns:
            A string representation of the prompt.
        """
        return self.summary()

    def input_signature(self) -> str:
        """Return a string representation of the prompt's input.

        Returns:
            A string representation of the prompt's input.
        """
        return (
            "("
            + ", ".join(
                [f"{param.name}: {type(self.template.input[param.name]).__name__}" for param in self.input_parameters]
            )
            + ")"
        )

    def output_signature(self) -> str:
        """Return a string representation of the prompt's output.

        Returns:
            A string representation of the prompt's output.
        """
        return (
            "("
            + ", ".join(
                [f"{param.name}: {type(self.template.output[param.name]).__name__}" for param in self.output_parameters]
            )
            + ")"
        )

    def function_signature(self) -> str:
        """Return a string representation of the prompt."""
        return f"{self.input_signature()} -> {self.output_signature()}"


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
        description="description of sample prompt",
        input_parameters=[
            ParameterInfo(name="input1", description="The first input parameter."),
            ParameterInfo(name="input2", description="The second input parameter."),
        ],
        output_parameters=[
            ParameterInfo(name="output1", description="The first output parameter."),
            ParameterInfo(name="output2", description="The second output parameter."),
        ],
        template=IOExample(
            input={"input1": "Hello, world!", "input2": "Hello, world!"},
            output={"output1": "Hello, world!", "output2": "Hello, world!"},
        ),
        examples=[
            IOExample(
                input={"input1": "Hello, world!", "input2": "Hello, world!"},
                output={"output1": "Hello, world!", "output2": "Hello, world!"},
            ),
            IOExample(
                input={"input1": "Hello, world!", "input2": "Hello, world!"},
                output={"output1": "Hello, world!", "output2": "Hello, world!"},
            ),
        ],
    )
