from abc import ABC, abstractmethod

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, Prompt


class ExampleReasoning(DataClass):
    """A reasoning for a prompt."""

    reasoning: str


class ReasoningTemplate(DataClass):
    template: str


class ReasoningExtractor(ABC):
    """Extracts reasoning from a prompt."""

    @abstractmethod
    def generate_reasoning(self, prompt: Prompt, example: Example) -> ExampleReasoning:
        pass  # pragma: no cover

    @abstractmethod
    def get_reasoning_template(self) -> str:
        pass  # pragma: no cover
