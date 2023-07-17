import json
from typing import List, Optional, Tuple

from promptgen.model.input_formatter import InputFormatter, InputValue
from promptgen.model.output_formatter import OutputFormatter, OutputValue
from promptgen.prompt_formatter.prompt_formatter import PromptFormatter


class JsonPromptFormatter(PromptFormatter):
    def __init__(self, strict: bool = True):
        super().__init__(JsonInputFormatter(), JsonOutputFormatter(strict=strict))


class JsonInputFormatter(InputFormatter):
    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        return with_code_block("json", json.dumps(input, ensure_ascii=False))


class JsonOutputFormatter(OutputFormatter):
    """The json output formatter.

    Args:
        strict (bool, optional): Whether to check if the output starts and ends with ```json. Defaults to True.
        indent (int | None, optional): The indent to use. Defaults to 1.
    """

    strict: bool
    indent: Optional[int]

    def __init__(self, strict: bool = True, indent: Optional[int] = 1):
        self.strict = strict
        self.indent = indent

    def description(self) -> str:
        """The description of the json output formatter."""

        return """Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json."""

    def format(self, output: OutputValue) -> str:
        """Format the output value into a string.

        Args:
            output (OutputValue): The output value.

        Raises:
            TypeError: If the output is not a dict.

        Returns:
            str: The formatted output.
        """
        if not isinstance(output, dict):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(output).__name__}.")

        return with_code_block("json", json.dumps(output, ensure_ascii=False, indent=self.indent))

    def parse(self, output_keys: List[Tuple[str, type]], output: str) -> OutputValue:
        output = output.strip()

        if self.strict:
            if not output.startswith("```json"):
                raise ValueError("Expected output to start with ```json.")
            if not output.endswith("```"):
                raise ValueError("Expected output to end with ```.")

        resp = json.loads(remove_code_block("json", output))

        for key, _ in output_keys:
            if key not in resp:
                raise ValueError(f"Expected output to have key {key}.")

        return resp


def with_code_block(language: str, s: str) -> str:
    """Wrap the string in a code block.

    Args:
        language (str): The language of the code block.
        s (str): The string to wrap.

    Returns:
        str: The string wrapped in a code block.
    """
    return f"```{language}\n{s}```"


def remove_code_block(language: str, s: str) -> str:
    """Remove the code block from the string.

    Args:
        language (str): The language of the code block.
        s (str): The string to remove the code block from.

    Returns:
        str: The string without the code block.
    """
    return s.replace(f"```{language}", "").replace("```", "").strip()
