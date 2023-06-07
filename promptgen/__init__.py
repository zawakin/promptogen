from __future__ import annotations

__version__ = "0.1.0"

from .input import InputFormatter, InputValue, JsonInputFormatter, KeyValueInputFormatter
from .output import JsonOutputFormatter, KeyValueOutputFormatter, OutputFormatter, OutputValue
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
