from __future__ import annotations

__version__ = "0.1.0"

from .input_formatter import InputFormatter, InputValue
from .output_formatter import OutputFormatter, OutputValue
from .prompt import (
    Example,
    ParameterInfo,
    Prompt,
    create_sample_prompt,
    load_prompt_from_dict,
    load_prompt_from_json_file,
    load_prompt_from_json_string,
)
from .prompt_collection import PromptCollection
from .prompt_formatters.json_formatter import JsonInputFormatter, JsonOutputFormatter, JsonPromptFormatter
from .prompt_formatters.key_value_formatter import (
    KeyValueInputFormatter,
    KeyValueOutputFormatter,
    KeyValuePromptFormatter,
)
from .prompt_formatters.prompt_formatter import PromptFormatter, PromptFormatterInterface
from .prompt_formatters.text_formatter import TextOutputFormatter

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
