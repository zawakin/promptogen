from abc import ABC, abstractmethod

from promptgen.model.prompt import Prompt


class PromptTransformer(ABC):
    @abstractmethod
    def transform_prompt(self, prompt: Prompt) -> Prompt:
        pass  # pragma: no cover
