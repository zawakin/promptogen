from __future__ import annotations

__version__ = "0.1.0"

from .input import (
    CodeInputFormatter,
    InputFormatter,
    InputValue,
    JsonInputFormatter,
    KeyValueInputFormatter,
    TextInputFormatter,
)
from .output import (
    CodeOutputFormatter,
    JsonOutputFormatter,
    KeyValueOutputFormatter,
    OutputFormatter,
    OutputValue,
    TextOutputFormatter,
)
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
from .prompt_formatter import JsonPromptFormatter, KeyValuePromptFormatter, PromptFormatter, PromptFormatterInterface

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
    # code
    "CodeInputFormatter",
    "CodeOutputFormatter",
    # raw
    "TextInputFormatter",
    "TextOutputFormatter",
    # list
    "KeyValueInputFormatter",
    "KeyValueOutputFormatter",
    "KeyValuePromptFormatter",
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
