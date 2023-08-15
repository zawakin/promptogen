from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from promptogen.model.dataclass import DataClass
from promptogen.model.prompt import IOExample, ParameterInfo, Prompt
from promptogen.model.value_formatter import Value, ValueFormatter


class PromptFormatterInterface(ABC):
    """Interface for formatting a prompt and parsing the output of the prompt."""

    @abstractmethod
    def format_prompt(self, prompt: Prompt, input_value: Value) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def format_prompt_without_input(self, prompt: Prompt) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def parse(self, prompt: Prompt, output: str) -> Value:
        pass  # pragma: no cover


class PromptFormatterConfig(DataClass):
    """Configuration for formatting a prompt.

    Attributes:
        show_formatter_description (bool): Whether to show the description of the formatter.
        show_parameter_info (bool): Whether to show the parameter info of the prompt.
        show_template (bool): Whether to show the template of the prompt.
    """

    show_formatter_description: bool = True
    show_parameter_info: bool = True
    show_template: bool = True


class PromptFormatter(PromptFormatterInterface):
    """Format a prompt and parse the output of the prompt.

    Args:
        input_formatter (ValueFormatter): Formatter for input.
        output_formatter (ValueFormatter): Formatter for output.
        config (PromptFormatterConfig, optional): Configuration for formatting. Defaults to PromptFormatterConfig().

    Raises:
        TypeError: If input_formatter or output_formatter is not an instance of ValueFormatter.
    """

    input_formatter: ValueFormatter
    output_formatter: ValueFormatter
    config: PromptFormatterConfig

    def __init__(
        self,
        *,
        input_formatter: ValueFormatter,
        output_formatter: ValueFormatter,
        config: PromptFormatterConfig = PromptFormatterConfig(),
    ):
        if not isinstance(input_formatter, ValueFormatter):
            raise TypeError(
                f"input_formatter must be an instance of ValueFormatter, got {type(input_formatter).__name__}."
            )
        if not isinstance(output_formatter, ValueFormatter):
            raise TypeError(
                f"output_formatter must be an instance of OutputFormatter, got {type(output_formatter).__name__}."
            )

        self.input_formatter = input_formatter
        self.output_formatter = output_formatter
        self.config = config

    def format_prompt(self, prompt: Prompt, input_value: Value) -> str:
        """Format a prompt with the given input value.

        Args:
            prompt (Prompt): Prompt to format.
            input_value (Value): Input value to format.

        Returns:
            str: Formatted prompt.

        Raises:
            TypeError: If input_value is not an instance of dict.
            TypeError: If prompt is not an instance of Prompt.
        """
        if not isinstance(input_value, dict):
            raise TypeError(f"Expected input_value to be an instance of dict, got {type(input_value).__name__}.")
        if not isinstance(prompt, Prompt):
            raise TypeError(f"Expected prompt to be an instance of Prompt, got {type(prompt).__name__}.")

        input_parameter_keys = {p.name for p in prompt.input_parameters}
        if input_parameter_keys != input_value.keys():
            raise ValueError(
                f"Expected input_value to have the same keys as prompt.input_parameters, got {input_value.keys()}; wanted {input_parameter_keys}."
            )

        input_value = {p.name: input_value[p.name] for p in prompt.input_parameters}
        return f"""{self.format_prompt_without_input(prompt)}
--------

Input:
{self.input_formatter.format(input_value)}
Output:"""

    def format_prompt_without_input(self, prompt: Prompt) -> str:
        """Format a prompt without input.

        Args:
            prompt (Prompt): Prompt to format.

        Returns:
            str: Formatted prompt.

        Raises:
            TypeError: If prompt is not an instance of Prompt.
        """
        # use config to determine what to show

        ss = [prompt.description]
        if self.config.show_formatter_description:
            ss.append(self.output_formatter.description())

        if self.config.show_parameter_info:
            ss.append(f"""Input Parameters:\n{self._format_parameter_infos(prompt.input_parameters)}""")
            ss.append(f"""Output Parameters:\n{self._format_parameter_infos(prompt.output_parameters)}""")

        if self.config.show_template:
            ss.append(f"Template:\n{self._format_example(prompt.template)}")

        ss.append(self._format_examples(prompt.examples))

        return "\n\n".join(s for s in ss if s)

    def _format_examples(self, examples: List[IOExample]) -> str:
        return "\n".join(f"Example {i+1}:\n{self._format_example(e)}\n" for i, e in enumerate(examples))

    def _format_example(self, example: IOExample) -> str:
        formatted_input = self.input_formatter.format(example.input)
        formatted_output = self.output_formatter.format(example.output)
        return f"Input:\n{formatted_input}\nOutput:\n{formatted_output}"

    def _format_parameter_infos(self, parameters: List[ParameterInfo]) -> str:
        return "\n".join(f"  - {p.name}: {p.description}" for p in parameters)

    def parse(self, prompt: Prompt, s: str) -> Value:
        """Parse the output of the prompt.

        Args:
            prompt (Prompt): Prompt to parse.
            s (str): Output of the prompt.

        Returns:
            Value: Parsed output.
        """
        output_keys = [(param.name, type(prompt.template.output[param.name])) for param in prompt.output_parameters]
        return self.output_formatter.parse(output_keys, s)


def convert_dataclass_to_dict(value: Value) -> Value:
    """Convert a dataclass to a dict recursively."""
    if isinstance(value, dict):
        return {k: convert_dataclass_to_dict(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_dataclass_to_dict(v) for v in value]
    elif isinstance(value, DataClass):
        return value.to_dict()
    elif isinstance(value, BaseModel):
        return value.model_dump()
    else:
        return value
