from abc import ABC, abstractmethod

from promptgen.dataclass import DataClass

from .input import InputFormatter, InputValue, JsonInputFormatter, KeyValueInputFormatter
from .output import JsonOutputFormatter, KeyValueOutputFormatter, OutputFormatter, OutputValue
from .prompt import Example, Prompt


class PromptFormatterInterface(ABC):
    @abstractmethod
    def format_prompt(self, prompt: Prompt, input_value: InputValue) -> str:
        pass

    @abstractmethod
    def format_prompt_without_input(self, prompt: Prompt) -> str:
        pass

    @abstractmethod
    def parse(self, output: str) -> OutputValue:
        pass


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
                f"Expected input_formatter to be an instance of InputFormatter, got {type(input_formatter).__name__}."
                "Usage: JsonInputFormatter() instead of JsonInputFormatter."
                "If you want to use a custom input formatter, you can subclass InputFormatter and pass an instance of"
                "your subclass to the PromptFormatter constructor."
            )
        if not isinstance(output_formatter, OutputFormatter):
            raise TypeError(
                f"Expected output_formatter to be an instance of OutputFormatter, got {type(output_formatter).__name__}."
                "Usage: JsonOutputFormatter() instead of JsonOutputFormatter."
                "If you want to use a custom output formatter, you can subclass OutputFormatter and pass an instance of"
                "your subclass to the PromptFormatter constructor."
            )
        self.input_formatter = input_formatter
        self.output_formatter = output_formatter

    def format_prompt(self, prompt: Prompt, input_value: InputValue) -> str:
        if not isinstance(input_value, InputValue):
            raise TypeError(f"Expected input_value to be an instance of InputValue, got {type(input_value).__name__}.")
        if not isinstance(prompt, Prompt):
            raise TypeError(f"Expected prompt to be an instance of Prompt, got {type(prompt).__name__}.")
        input_parameter_keys = {p.name for p in prompt.input_parameters}
        if input_parameter_keys != input_value.dict().keys():
            raise ValueError(
                f"Expected input_value to have the same keys as prompt.input_parameters, got {input_value.dict().keys()}; wanted {input_parameter_keys}."
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
        formatted_template = self.format_example(prompt.template)
        formatted_examples = (
            "\n".join(f"Example {i+1}:\n{self.format_example(e)}\n" for i, e in enumerate(prompt.examples))
            if prompt.examples
            else ""
        )

        return f"""You are an AI named "{prompt.name}".
{prompt.description}
{self.output_formatter.description()}

Input Parameters:
{formatted_input_parameters}

Output Parameters:
{formatted_output_parameters}

Template:
{formatted_template}

{formatted_examples}"""

    def format_example(self, example: Example) -> str:
        formatted_input = self.input_formatter.format(example.input)
        formatted_output = self.output_formatter.format(example.output)
        return f"Input:\n{formatted_input}\nOutput:\n{formatted_output}"

    def parse(self, s: str) -> OutputValue:
        return self.output_formatter.parse(s)


class JsonPromptFormatter(PromptFormatter):
    def __init__(self):
        super().__init__(JsonInputFormatter(), JsonOutputFormatter())


class KeyValuePromptFormatter(PromptFormatter):
    def __init__(self):
        super().__init__(KeyValueInputFormatter(), KeyValueOutputFormatter())
