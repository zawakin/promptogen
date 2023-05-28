from abc import ABC, abstractmethod

from .input import InputFormatter, InputValue, JsonInputFormatter
from .output import JsonOutputFormatter, OutputFormatter, OutputValue
from .prompt import Example, Prompt

class PromptFormatter(ABC):
    @abstractmethod
    def format_prompt(self, prompt: Prompt, input_value: InputValue) -> str:
        pass

    @abstractmethod
    def format_prompt_without_input(self, prompt: Prompt) -> str:
        pass

    @abstractmethod
    def parse(self, output: str) -> OutputValue:
        pass


class BasePromptFormatter(PromptFormatter):
    input_formatter: InputFormatter
    output_formatter: OutputFormatter

    def __init__(
        self,
        input_formatter: InputFormatter = JsonInputFormatter(),
        output_formatter: OutputFormatter = JsonOutputFormatter(),
    ):
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
            "\n".join(
                f"Example {i+1}:\n{self.format_example(e)}\n"
                for i, e in enumerate(prompt.examples)
            )
            if prompt.examples
            else ""
        )

        formatted_input_parameters = "\n".join(
            f"  - {p.name}: {p.description}" for p in prompt.input_parameters
        )
        formatted_output_parameters = "\n".join(
            f"  - {p.name}: {p.description}" for p in prompt.output_parameters
        )

        return f"""You are an AI named "{prompt.name}".
{prompt.description}

Output a {self.output_formatter.name()}-formatted string without \
outputting any other strings.

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


class JsonPromptFormatter(BasePromptFormatter):
    def __init__(self):
        super().__init__(JsonInputFormatter(), JsonOutputFormatter())
