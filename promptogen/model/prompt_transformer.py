from abc import ABC, abstractmethod

from promptogen.model.prompt import Prompt


class PromptTransformer(ABC):
    """Transform a prompt. This is useful for various purposes, such as:
    - Adding reasoning output parameters to the prompt.
    - Adding examples to the prompt.
    - etc.
    """

    @abstractmethod
    def transform_prompt(self, prompt: Prompt) -> Prompt:
        pass  # pragma: no cover
