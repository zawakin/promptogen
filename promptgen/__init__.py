from __future__ import annotations

__version__ = "0.1.0"

from .model import (
    Example,
    InputFormatter,
    InputValue,
    OutputFormatter,
    OutputValue,
    ParameterInfo,
    Prompt,
    create_sample_prompt,
    load_prompt_from_dict,
    load_prompt_from_json_file,
    load_prompt_from_json_string,
)
from .prompt_collection import PromptCollection
from .prompt_formatter.json_formatter import JsonInputFormatter, JsonOutputFormatter, JsonPromptFormatter
from .prompt_formatter.key_value_formatter import (
    KeyValueInputFormatter,
    KeyValueOutputFormatter,
    KeyValuePromptFormatter,
)
from .prompt_formatter.prompt_formatter import PromptFormatter, PromptFormatterInterface
from .prompt_formatter.text_formatter import TextOutputFormatter

__all__ = [
    # common
    "InputValue",
    "OutputValue",
    "InputFormatter",
    "OutputFormatter",
    "PromptFormatter",
    # json
    "JsonInputFormatter",
    "JsonOutputFormatter",
    "JsonPromptFormatter",
    # list
    "KeyValueInputFormatter",
    "KeyValueOutputFormatter",
    "KeyValuePromptFormatter",
    # text
    "TextOutputFormatter",
    # prompt
    "Prompt",
    "ParameterInfo",
    "Example",
    "PromptFormatterInterface",
    "create_sample_prompt",
    # load
    "load_prompt_from_dict",
    "load_prompt_from_json_file",
    "load_prompt_from_json_string",
    "PromptCollection",
]
