from abc import ABC, abstractmethod
from typing import Callable


class LLM(ABC):
    """Language model interface."""

    pass  # pragma: no cover


class TextBasedLLM(LLM):
    """Language model interface that generates text."""

    @abstractmethod
    def generate(self, input_text: str) -> str:
        pass  # pragma: no cover


class TextBasedLLMWrapper(TextBasedLLM):
    def __init__(self, *, generate_text_by_text: Callable[[str], str]):
        self.generate_text_by_text = generate_text_by_text

    def generate(self, prompt: str) -> str:
        return self.generate_text_by_text(prompt)
