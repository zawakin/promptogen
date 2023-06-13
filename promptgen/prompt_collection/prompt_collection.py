from __future__ import annotations

from typing import Dict, List

from promptgen.prompt import Prompt

from ..prompts import load_predefined_prompts


class PromptCollection(Dict[str, Prompt]):
    # prompts: dict[str, Prompt] = {}

    def __init__(self, load_predefined: bool = True):
        # self.prompts = {}
        self.__dict__.update({})
        if load_predefined:
            for prompt in load_predefined_prompts():
                self.add_prompt(prompt)

    def get_prompt(self, name: str) -> Prompt:
        return self.__getitem__(name)

    def list_prompts(self) -> List[str]:
        return list(self.keys())

    def add_prompt(self, prompt: Prompt):
        if not isinstance(prompt, Prompt):
            raise Exception("Prompt must be an instance of Prompt")
        self.__setitem__(prompt.name, prompt)

    def __str__(self):
        s = ""
        s += "<PromptCollection>\n"
        s += f"Number of prompts: {len(self)}\n\n"
        s += "Prompts:\n"
        for _, prompt in self.items():
            s += f"- {prompt.__str__()}\n"

        return s

    def __repr__(self):
        return self.__str__()
