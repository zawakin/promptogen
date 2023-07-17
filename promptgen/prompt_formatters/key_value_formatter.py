import re
from ast import literal_eval
from pprint import pformat
from typing import Any, Callable, Dict, List, Tuple

from promptgen.input_formatter import InputFormatter, InputValue
from promptgen.output_formatter import OutputFormatter, OutputValue
from promptgen.prompt_formatters.prompt_formatter import PromptFormatter


def format_string(s: str) -> str:
    # escape double quotes
    s = s.replace('"', '\\"')

    if "\n" in s:
        return f'"""{s}"""'
    return f'"{s}"'


default_type_formatter: Dict[type, Callable[[Any], str]] = {
    str: format_string,
}


class ValueFormatter:
    type_formatter: Dict[type, Callable[[Any], str]]

    def __init__(self, type_formatter: Dict[type, Callable[[Any], str]] = {}):
        self.type_formatter = {**default_type_formatter, **type_formatter}

    def format(self, value: Any) -> str:
        if type(value) in self.type_formatter:
            return self.type_formatter[type(value)](value)
        else:
            return pformat(value, indent=2, sort_dicts=False, width=160)

    def parse(self, value: Any) -> Any:
        return value


class KeyValuePromptFormatter(PromptFormatter):
    def __init__(self, value_formatter: ValueFormatter = ValueFormatter()):
        super().__init__(
            KeyValueInputFormatter(value_formatter), KeyValueOutputFormatter(value_formatter=value_formatter)
        )


class KeyValueInputFormatter(InputFormatter):
    value_formatter: ValueFormatter

    def __init__(self, value_formatter: ValueFormatter = ValueFormatter()):
        self.value_formatter = value_formatter

    def format(self, input: InputValue) -> str:
        if not isinstance(input, dict):
            raise TypeError(f"Expected input to be an instance of InputValue, got {type(input).__name__}.")

        s = ""
        for key, value in input.items():
            s += f"{key}: {self.value_formatter.format(value)}\n"

        return s.strip()


class KeyValueOutputFormatter(OutputFormatter):
    value_formatter: ValueFormatter

    def __init__(self, value_formatter: ValueFormatter = ValueFormatter()):
        self.value_formatter = value_formatter

    def description(self) -> str:
        return ""

    def format(self, output: OutputValue) -> str:
        if not isinstance(output, dict):
            raise TypeError(f"Expected output to be an instance of OutputValue, got {type(output).__name__}.")

        s = ""
        for key, value in output.items():
            s += f"{key}: {self.value_formatter.format(value)}\n"

        return s.strip()

    def parse(self, output_keys: List[Tuple[str, type]], output: str) -> OutputValue:
        if not isinstance(output, str):
            raise TypeError(f"Expected formatted_str to be a str, got {type(output).__name__}.")

        for key, _ in output_keys:
            if key not in output:
                raise ValueError(f"Expected output to have key {key}.")

        if len(output_keys) == 0:
            raise ValueError("Expected output_keys to have at least one key.")

        result = {}

        for idx, (key, key_type) in enumerate(output_keys):
            next_key = output_keys[idx + 1][0] if idx + 1 < len(output_keys) else None
            if next_key:
                pattern = re.compile(f"{key}:.*?(?={next_key}:)", re.MULTILINE | re.DOTALL)
            else:
                pattern = re.compile(f"{key}:.*", re.MULTILINE | re.DOTALL)
            value = re.search(pattern, output)
            if value is None:
                raise ValueError(f"Expected output to have key {key}.")

            m: re.Match[str] = value
            s = m.group().replace(f"{key}:", "").strip()

            if key_type == str:
                extracted_str, found = extract_string(s)
                if found:
                    result[key] = extracted_str
                else:
                    raise SyntaxError(f"invalid syntax for key {key}: {s}")
            else:
                result[key] = literal_eval(s)

        return result


def extract_string(s: str) -> Tuple[str, bool]:
    quotes_flags = [
        ("'''", re.DOTALL),
        ('"""', re.DOTALL),
        ("'", 0),
        ('"', 0),
    ]

    for quote, flag in quotes_flags:
        if not s.startswith(quote):
            continue
        match = re.search(f"{quote}(.*?){quote}", s, flag)
        if match:
            return match.group(1), True
        else:
            return "", False

    # If no quotes are found, return the original string.
    return s, True
