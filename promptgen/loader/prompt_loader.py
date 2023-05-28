from promptgen.prompt import Prompt
from ..prompts.text_summarizer import TextSummarizer
from ..prompts.text_categorizer import TextCategorizer
from ..prompts.prompt_example_creator import PromptExampleCreator
from ..prompts.prompt_creator import PromptCreator
from ..prompts.prompt_optimizer import PromptOptimizer


class PromptLoader:
    prompts: dict[str, Prompt] = {}

    def __init__(self):
        self.load_prompts()

    def load_prompts(self):
        prompts = [
            TextSummarizer(),
            TextCategorizer(),
            PromptExampleCreator(),
            PromptCreator(),
            PromptOptimizer(),
        ]

        for prompt in prompts:
            self.add_prompt(prompt)

    def get_prompt(self, name: str) -> Prompt:
        return self.prompts[name].copy(deep=True)

    def add_prompt(self, prompt: Prompt):
        self.prompts[prompt.name] = prompt

    def __call__(self, name: str) -> Prompt:
        return self.get_prompt(name)

    def __str__(self):
        s = ""
        s += "Available prompts:\n"
        for name, prompt in self.prompts.items():
            s += f"- {name}: {prompt.description}\n"

        return s

    def __repr__(self):
        return self.__str__()
