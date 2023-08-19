from __future__ import annotations

from importlib import metadata

from .model import (
    DataClass,
    FunctionBasedTextLLM,
    IOExample,
    ParameterInfo,
    Prompt,
    PromptRunner,
    TextLLM,
    TextLLMPromptRunner,
    Value,
)
from .prompt_formatter import (
    JsonPromptFormatter,
    KeyValuePromptFormatter,
    PromptFormatter,
    PromptFormatterConfig,
    PromptFormatterInterface,
)

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    # dataclass
    "DataClass",
    # llm
    "TextLLM",
    "FunctionBasedTextLLM",
    # prompt formatter
    "JsonPromptFormatter",
    "KeyValuePromptFormatter",
    "PromptFormatter",
    # prompt
    "Value",
    "Prompt",
    "ParameterInfo",
    "IOExample",
    "PromptFormatterConfig",
    "PromptFormatterInterface",
    # prompt runner
    "PromptRunner",
    "TextLLMPromptRunner",
]
