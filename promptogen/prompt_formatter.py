from abc import ABC, abstractmethod
from .input import InputFormatter, InputValue
from .output import OutputFormatter, OutputValue
from .prompt import Example, Prompt


class PromptFormatter(ABC):
    @abstractmethod
    def format(self, inputValue: InputValue, inputFormatter: InputFormatter, outputFormatter: OutputFormatter) -> str:
        pass

    @abstractmethod
    def parse(self, output: str, outputFormatter: OutputFormatter) -> OutputValue:
        pass


class BasePromptFormatter(PromptFormatter):
    model: Prompt

    def __init__(self, *, model: Prompt | dict):
        if isinstance(model, dict):
            self.model = Prompt.from_dict(model)
        else:
            self.model = model

    def format(self, input: InputValue, inputFormatter: InputFormatter, outputFormatter: OutputFormatter) -> str:
        formatted_input = inputFormatter.format(input)
        formatted_template = self.format_example(
            self.model.template, inputFormatter, outputFormatter)
        formatted_examples = "\n".join(
            f'Example {i+1}:\n{self.format_example(e, inputFormatter, outputFormatter)}\n' for i, e in enumerate(self.model.examples)) if self.model.examples else ""

        formatted_input_parameters = "\n".join(
            f"  - {p.name}: {p.description}" for p in self.model.input_parameters
        )
        formatted_output_parameters = "\n".join(
            f"  - {p.name}: {p.description}" for p in self.model.output_parameters
        )

        return (
            f'''You are an AI named "{self.model.name}".
{self.model.description}

Output a {outputFormatter.name()}-formatted string without outputting any other strings.

Input Parameters:
{formatted_input_parameters}

Output Parameters:
{formatted_output_parameters}

Template:
{formatted_template}

{formatted_examples}

Input:
{formatted_input}
Output:'''
        )

    def format_example(self, example: Example, inputFormatter: InputFormatter, outputFormatter: OutputFormatter) -> str:
        formatted_input = inputFormatter.format(example.input)
        formatted_output = outputFormatter.format(example.output)
        return f"Input:\n{formatted_input}\nOutput:\n{formatted_output}"

    def parse(self, s: str, outputFormatter: OutputFormatter) -> OutputValue:
        return outputFormatter.parse(s)
