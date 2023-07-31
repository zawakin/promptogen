from __future__ import annotations

from typing import Dict

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Prompt

from .predefined_prompts import load_predefined_prompts


class PromptCollection(DataClass):
    prompts: Dict[str, Prompt] = {}


class PredefinedPromptCollection(PromptCollection):
    prompts: Dict[str, Prompt] = {prompt.name: prompt for prompt in load_predefined_prompts()}
