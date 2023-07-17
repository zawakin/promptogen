from pprint import pformat
from typing import Any, Callable, Dict


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
