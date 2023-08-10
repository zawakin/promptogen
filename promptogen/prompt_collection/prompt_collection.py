from __future__ import annotations

from typing import Dict

from promptogen.model.dataclass import DataClass
from promptogen.model.prompt import Prompt

from .predefined_prompts import load_predefined_prompts


class PromptCollection(DataClass):
    """Collection of prompts."""

    prompts: Dict[str, Prompt] = {}

    def __repr__(self) -> str:
        prompt_names = list(self.prompts.keys())[:20]
        return f"{self.__class__.__name__}(prompt_names={prompt_names!r})"

    def __str__(self) -> str:
        return self.summary()

    def summary(self) -> str:
        def section_header(title):
            return f"\n{title}\n" + "-" * len(title)

        prompt_overview = section_header("Prompts Overview")
        for name, prompt in self.prompts.items():
            prompt_overview += f"\n  {name}: {prompt.function_signature()}"

        return f"{prompt_overview}\n\nUse 'details()' method to view full details of each prompt."

    def details(self) -> str:
        def section_header(title):
            return f"\n{title}\n" + "-" * len(title)

        prompt_details = section_header("Prompts Details")
        for name, prompt in self.prompts.items():
            prompt_details += f"\n  {name}: {prompt.description}\n"

        return f"{prompt_details}"

    @classmethod
    def load_predefined(cls) -> PromptCollection:
        """Load the prompt collection."""
        return cls(prompts={prompt.name: prompt for prompt in load_predefined_prompts()})
