from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, ParameterInfo, Prompt
from promptgen.model.value_formatter import Value, ValueFormatter


class PromptFormatterInterface(ABC):
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
    show_formatter_description: bool = True
    show_parameter_info: bool = True
    show_template: bool = True
    show_examples: bool = True


class PromptFormatter(PromptFormatterInterface):
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
        if not isinstance(input_value, dict):
            raise TypeError(f"Expected input_value to be an instance of dict, got {type(input_value).__name__}.")
        if not isinstance(prompt, Prompt):
            raise TypeError(f"Expected prompt to be an instance of Prompt, got {type(prompt).__name__}.")

        input_parameter_keys = {p.name for p in prompt.input_parameters}
        if input_parameter_keys != input_value.keys():
            raise ValueError(
                f"Expected input_value to have the same keys as prompt.input_parameters, got {input_value.keys()}; wanted {input_parameter_keys}."
            )
        return f"""{self.format_prompt_without_input(prompt)}
--------

Input:
{self.input_formatter.format(input_value)}
Output:"""

    def format_prompt_without_input(self, prompt: Prompt) -> str:
        # use config to determine what to show

        ss = [prompt.description]
        if self.config.show_formatter_description:
            ss.append(self.output_formatter.description())

        if self.config.show_parameter_info:
            ss.append(f"""Input Parameters:\n{self._format_parameter_infos(prompt.input_parameters)}""")
            ss.append(f"""Output Parameters:\n{self._format_parameter_infos(prompt.output_parameters)}""")

        if self.config.show_template:
            ss.append(f"Template:\n{self._format_example(prompt.template)}")

        if self.config.show_examples:
            ss.append(self._format_examples(prompt.examples))

        return "\n\n".join(s for s in ss if s)

    def _format_examples(self, examples: List[Example]) -> str:
        return "\n".join(f"Example {i+1}:\n{self._format_example(e)}\n" for i, e in enumerate(examples))

    def _format_example(self, example: Example) -> str:
        formatted_input = self.input_formatter.format(example.input)
        formatted_output = self.output_formatter.format(example.output)
        return f"Input:\n{formatted_input}\nOutput:\n{formatted_output}"

    def _format_parameter_infos(self, parameters: List[ParameterInfo]) -> str:
        return "\n".join(f"  - {p.name}: {p.description}" for p in parameters)

    def parse(self, prompt: Prompt, s: str) -> Value:
        output_keys = [(param.name, type(prompt.template.output[param.name])) for param in prompt.output_parameters]
        return self.output_formatter.parse(output_keys, s)
