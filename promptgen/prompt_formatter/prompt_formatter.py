from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from promptgen.model.dataclass import DataClass
from promptgen.model.input_formatter import InputFormatter, InputValue
from promptgen.model.output_formatter import OutputFormatter, OutputValue
from promptgen.model.prompt import Example, Prompt


class PromptFormatterInterface(ABC):
    @abstractmethod
    def format_prompt(self, prompt: Prompt, input_value: InputValue) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def format_prompt_without_input(self, prompt: Prompt) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def parse(self, prompt: Prompt, output: str) -> OutputValue:
        pass  # pragma: no cover


class PromptFormatter(PromptFormatterInterface):
    input_formatter: InputFormatter
    output_formatter: OutputFormatter

    def __init__(
        self,
        input_formatter: InputFormatter,
        output_formatter: OutputFormatter,
    ):
        if not isinstance(input_formatter, InputFormatter):
            raise TypeError(
                f"input_formatter must be an instance of InputFormatter, got {type(input_formatter).__name__}."
            )
        if not isinstance(output_formatter, OutputFormatter):
            raise TypeError(
                f"output_formatter must be an instance of OutputFormatter, got {type(output_formatter).__name__}."
            )

        self.input_formatter = input_formatter
        self.output_formatter = output_formatter

    def format_prompt(self, prompt: Prompt, input_value: InputValue) -> str:
        if not isinstance(input_value, dict):
            raise TypeError(f"Expected input_value to be an instance of dict, got {type(input_value).__name__}.")
        if not isinstance(prompt, Prompt):
            raise TypeError(f"Expected prompt to be an instance of Prompt, got {type(prompt).__name__}.")

        input_parameter_keys = {p.name for p in prompt.input_parameters}
        if input_parameter_keys != input_value.keys():
            raise ValueError(
                f"Expected input_value to have the same keys as prompt.input_parameters, got {input_value.keys()}; wanted {input_parameter_keys}."
            )
        formatted_input = self.input_formatter.format(input_value)
        return f"""{self.format_prompt_without_input(prompt)}
--------

Input:
{formatted_input}
Output:"""

    def format_prompt_without_input(self, prompt: Prompt) -> str:
        formatted_input_parameters = "\n".join(f"  - {p.name}: {p.description}" for p in prompt.input_parameters)
        formatted_output_parameters = "\n".join(f"  - {p.name}: {p.description}" for p in prompt.output_parameters)
        formatted_template = self._format_example(prompt.template)
        formatted_examples = (
            "\n".join(f"Example {i+1}:\n{self._format_example(e)}\n" for i, e in enumerate(prompt.examples))
            if prompt.examples
            else ""
        )

        return f"""{prompt.description}
{self.output_formatter.description()}

Input Parameters:
{formatted_input_parameters}

Output Parameters:
{formatted_output_parameters}

Template:
{formatted_template}

{formatted_examples}"""

    def _format_example(self, example: Example) -> str:
        formatted_input = self.input_formatter.format(example.input)
        formatted_output = self.output_formatter.format(example.output)
        return f"Input:\n{formatted_input}\nOutput:\n{formatted_output}"

    def parse(self, prompt: Prompt, s: str) -> OutputValue:
        output_keys = prompt.get_output_keys()
        return self.output_formatter.parse(output_keys, s)