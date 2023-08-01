from abc import ABC, abstractmethod
from typing import Callable


class LLM(ABC):
    """Language model interface."""

    pass  # pragma: no cover


class TextBasedLLM(LLM, ABC):
    """Language model interface that generates text."""

    @abstractmethod
    def generate(self, input_text: str) -> str:
        pass  # pragma: no cover


class TextBasedLLMWrapper(TextBasedLLM):
    """Text-based language model wrapper.
    It wraps a function that generates text by the given text.

    Args:
        generate_text_by_text: (input_text: str) -> (output_text: str)
                                A function that generates text by the given text.
    """

    def __init__(self, *, generate_text_by_text: Callable[[str], str]):
        if not callable(generate_text_by_text):
            raise TypeError("generate_text_by_text must be callable")
        self._gen = generate_text_by_text

    def generate(self, input_text: str) -> str:
        return self._gen(input_text)
