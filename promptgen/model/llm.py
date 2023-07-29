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
    def __init__(self, *, generate_llm_response: Callable[[str], str]):
        self.generate_llm_response = generate_llm_response

    def generate(self, prompt: str) -> str:
        return self.generate_llm_response(prompt)
