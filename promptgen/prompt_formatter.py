from abc import ABC, abstractmethod

from .input import CodeInputFormatter, InputFormatter, InputValue, JsonInputFormatter
from .output import CodeOutputFormatter, JsonOutputFormatter, OutputFormatter, OutputValue
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
        input_formatter: InputFormatter = JsonInputFormatter(),
        output_formatter: OutputFormatter = JsonOutputFormatter(),
    ):
        if not isinstance(input_formatter, InputFormatter):
            raise TypeError(f"Expected input_formatter to be an InputFormatter, got {type(input_formatter).__name__}.")
        if not isinstance(output_formatter, OutputFormatter):
            raise TypeError(
                f"Expected output_formatter to be an OutputFormatter, got {type(output_formatter).__name__}."
            )
        self.input_formatter = input_formatter
        self.output_formatter = output_formatter

    def format_prompt(self, prompt: Prompt, input_value: InputValue) -> str:
        formatted_input = self.input_formatter.format(input_value)
        return f"""{self.format_prompt_without_input(prompt)}

Input:
{formatted_input}
Output:"""

    def format_prompt_without_input(self, prompt: Prompt) -> str:
        formatted_template = self.format_example(prompt.template)
        formatted_examples = (
            "\n".join(f"Example {i+1}:\n{self.format_example(e)}\n" for i, e in enumerate(prompt.examples))
            if prompt.examples
            else ""
        )

        formatted_input_parameters = "\n".join(
            f"  - {name}: {p.description}" for name, p in prompt.input_parameters.items()
        )
        formatted_output_parameters = "\n".join(
            f"  - {name}: {p.description}" for name, p in prompt.output_parameters.items()
        )

        return f"""You are an AI named "{prompt.name}".
{prompt.description}

Output a {self.output_formatter.name()}-formatted string without \
outputting any other strings.
{self.output_formatter.constraints()}

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
