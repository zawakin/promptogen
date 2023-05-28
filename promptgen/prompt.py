from typing import Any

from pydantic import root_validator

from .dataclass import DataClass
from .input import InputValue
from .output import OutputValue


class ParameterInfo(DataClass):
    """Information about a parameter.

    Attributes:
        description: A description of the parameter.
    """

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
        input_parameters: The parameter information of the prompt's input.
        output_parameters: The parameter information of the prompt's output.
        template: An example of the prompt.
        examples: A list of examples of the prompt.
    """

    name: str
    description: str
    input_parameters: dict[str, ParameterInfo]
    output_parameters: dict[str, ParameterInfo]
    template: Example
    examples: list[Example]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Prompt":
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
        return cls.parse_obj(d)

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
        return cls.parse_raw(json_string)

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
            return cls.parse_raw(f.read())

    def to_json_file(self, filename: str, indent=4) -> None:
        with open(filename, "w") as f:
            f.write(self.json(indent=indent, ensure_ascii=False))

    @root_validator
    def validate_template(cls, values):
        template = values.get("template")
        input_parameters = values.get("input_parameters")
        output_parameters = values.get("output_parameters")

        if template is None or input_parameters is None or output_parameters is None:
            raise ValueError(
                "Template, input parameters, " "and output parameters must be provided"
            )

        if template.input.keys() != input_parameters.keys():
            raise ValueError(
                f"Template input keys do not match input parameters: "
                f"{template.input.keys()} vs {input_parameters}"
            )
        if template.output.keys() != output_parameters.keys():
            raise ValueError(
                f"Template output keys do not match output parameters: "
                f"{template.output.keys()} vs {output_parameters}"
            )

        return values

    @root_validator
    def validate_examples(cls, values):
        examples = values.get("examples")
        input_parameters = values.get("input_parameters")
        output_parameters = values.get("output_parameters")

        if examples is None or input_parameters is None or output_parameters is None:
            raise ValueError(
                "Examples, input parameters, " "and output parameters must be provided"
            )

        for example in examples:
            if example.input.keys() != input_parameters.keys():
                raise ValueError(
                    f"Example input keys do not match input parameters: "
                    f"{example.input.keys()} vs {input_parameters}"
                )
            if example.output.keys() != output_parameters.keys():
                raise ValueError(
                    f"Example output keys do not match output parameters: "
                    f"{example.output.keys()} vs {output_parameters}"
                )

        return values

    def with_examples(self, examples: list[Example] | list[dict]) -> "Prompt":
        """Set the examples of the prompt.

        Args:
            examples: The examples to set.

        Returns:
            A copy of the prompt with the examples set.
        """
        exs = [Example(**ex) if isinstance(ex, dict) else ex for ex in examples]
        return self.copy(deep=True, update={"examples": exs})

    def __repr__(self) -> str:
        return self.json(indent=4, ensure_ascii=False)

    def __str__(self) -> str:
        """Return a string representation of the prompt.

        Returns:
            A string representation of the prompt.
        """
        input_str = ", ".join(
            [f"{name}" for name, param in self.input_parameters.items()]
        )
        output_str = ", ".join(
            [f"{name}" for name, param in self.output_parameters.items()]
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


def load_prompt_from_dict(d: dict[str, Any]) -> Prompt:
    """Load a prompt from a dictionary.

    Args:
        d: The dictionary to load the prompt from.

    Returns:
        The loaded prompt.
    """
    return Prompt.from_dict(d)
