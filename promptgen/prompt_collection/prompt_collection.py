from __future__ import annotations

from promptgen.prompt import Prompt

from ..prompts import load_predefined_prompts


class PromptCollection:
    prompts: dict[str, Prompt] = {}

    def __init__(self, load_predefined: bool = True):
        if load_predefined:
            for prompt in load_predefined_prompts():
                self.add_prompt(prompt)

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
