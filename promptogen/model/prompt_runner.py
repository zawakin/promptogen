from abc import ABC, abstractmethod

from promptogen.model.llm import TextLLM
from promptogen.model.prompt import Prompt
from promptogen.model.value_formatter import Value
from promptogen.prompt_formatter.prompt_formatter import PromptFormatter


class PromptRunner(ABC):
    """A prompt runner is responsible for running a prompt and returning the result."""

    @abstractmethod
    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        pass  # pragma: no cover


class TextLLMPromptRunner(PromptRunner):
    """A text-based prompt runner is responsible for running a prompt and returning the result."""

    def __init__(self, llm: TextLLM, formatter: PromptFormatter):
        """Initialize a TextBasedPromptRunner.

        Args:
            llm: The LLM to use. It must be an instance of TextBasedLLM.
            formatter: The prompt formatter to use. It must be an instance of PromptFormatter.
        """
        self.text_llm = llm
        self.formatter = formatter

    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        """Run the given prompt and return the result.

        Args:
            prompt: The prompt to run. It must be an instance of Prompt.
            input_value: The input value to use. It must be an instance of Value, which is a dict.
        """
        raw_req = self.formatter.format_prompt(prompt, input_value)
        raw_resp = self.text_llm.generate(raw_req)
        resp = self.formatter.parse(prompt, raw_resp)
        return resp
