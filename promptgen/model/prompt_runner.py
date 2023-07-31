from abc import ABC, abstractmethod

from promptgen.model.llm import TextBasedLLM
from promptgen.model.prompt import Prompt
from promptgen.model.value_formatter import Value
from promptgen.prompt_formatter.prompt_formatter import PromptFormatter


class PromptRunner(ABC):
    """A prompt runner is responsible for running a prompt and returning the result."""

    @abstractmethod
    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        pass  # pragma: no cover


class TextBasedPromptRunner(PromptRunner):
    """A text-based prompt runner is responsible for running a prompt and returning the result."""

    def __init__(self, llm: TextBasedLLM, formatter: PromptFormatter):
        self.text_based_llm = llm
        self.formatter = formatter

    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        raw_req = self.formatter.format_prompt(prompt, input_value)
        raw_resp = self.text_based_llm.generate(raw_req)
        resp = self.formatter.parse(prompt, raw_resp)
        return resp
