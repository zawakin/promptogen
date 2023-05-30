from typing import Any
from promptgen.prompt import Prompt

from ..prompts import (
    get_example_creator_template,
    get_prompt_creator_template,
    get_prompt_optimizer_template,
    get_text_categorizer_template,
    get_text_summarizer_template,
)

class PromptCollection():
    prompts: dict[str, Prompt] = {}

    def __init__(self, load_predefined_prompts: bool = True):
        if load_predefined_prompts:
            self.load_predefined_prompts()

    def get_prompt(self, name: str) -> Prompt:
        if name not in self.prompts:
            raise Exception(f"Prompt {name} not found")
        return self.prompts[name].copy(deep=True)

    def list_prompts(self) -> list[str]:
        return list(self.prompts.keys())

    def add_prompt(self, prompt: Prompt):
        if not isinstance(prompt, Prompt):
            raise Exception("Prompt must be an instance of Prompt")
        self.__setitem__(prompt.name, prompt)

    def __getitem__(self, name: str) -> Prompt:
        if name not in self.prompts:
            raise Exception(f"Prompt {name} not found")
        return self.get_prompt(name)

    def __setitem__(self, name: str, prompt: Prompt):
        if not isinstance(prompt, Prompt):
            raise Exception("Prompt must be an instance of Prompt")
        self.prompts[name] = prompt

    def __contains__(self, name: str) -> bool:
        return name in self.prompts

    def __delitem__(self, name: str):
        if name not in self.prompts:
            raise Exception(f"Prompt {name} not found")
        del self.prompts[name]

    def __iter__(self):
        return iter(self.prompts)

    def __len__(self):
        return len(self.prompts)

    def __str__(self):
        s = ""
        s += "Available prompts:\n"
        for name, prompt in self.prompts.items():
            s += f"- {name}: {prompt.description}\n"

        return s

    def __repr__(self):
        return self.__str__()

    def load_predefined_prompts(self):
        prompts = [
            get_text_categorizer_template(),
            get_text_summarizer_template(),
            get_example_creator_template(),
            get_prompt_creator_template(),
            get_prompt_optimizer_template(),
        ]

        for prompt in prompts:
            self.add_prompt(prompt)
