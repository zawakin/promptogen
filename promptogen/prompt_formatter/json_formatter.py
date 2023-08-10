import json
from typing import List, Optional, Tuple

from promptogen.model.value_formatter import Value, ValueFormatter
from promptogen.prompt_formatter.prompt_formatter import (
    PromptFormatter,
    PromptFormatterConfig,
    convert_dataclass_to_dict,
)


class JsonPromptFormatter(PromptFormatter):
    def __init__(self, *, config: PromptFormatterConfig = PromptFormatterConfig(), strict: bool = True):
        super().__init__(
            input_formatter=JsonValueFormatter(), output_formatter=JsonValueFormatter(strict=strict), config=config
        )


class JsonValueFormatter(ValueFormatter):
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

    def format(self, value: Value) -> str:
        """Format the output value into a string.

        Args:
            output (OutputValue): The output value.

        Raises:
            TypeError: If the output is not a dict.

        Returns:
            str: The formatted output.
        """
        if not isinstance(value, dict):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(value).__name__}.")

        value = convert_dataclass_to_dict(value)

        return with_code_block("json", json.dumps(value, ensure_ascii=False, indent=self.indent))

    def parse(self, output_keys: List[Tuple[str, type]], output: str) -> Value:
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
