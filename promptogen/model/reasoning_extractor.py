from abc import ABC, abstractmethod

from promptogen.model.dataclass import DataClass
from promptogen.model.prompt import IOExample, Prompt


class ExampleReasoning(DataClass):
    """A reasoning for a prompt."""

    reasoning: str


class ReasoningExtractor(ABC):
    """Extracts reasoning from a prompt."""

    @abstractmethod
    def generate_reasoning(self, prompt: Prompt, example: IOExample) -> ExampleReasoning:
        pass  # pragma: no cover

    @abstractmethod
    def get_reasoning_template(self) -> str:
        pass  # pragma: no cover
