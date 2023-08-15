from abc import ABC, abstractmethod
from typing import List

from promptogen.model.llm import TextLLM
from promptogen.model.prompt import Prompt
from promptogen.model.prompt_interceptor import PromptInterceptor
from promptogen.model.value_formatter import Value
from promptogen.prompt_formatter.prompt_formatter import PromptFormatter


class PromptRunner(ABC):
    """A prompt runner is responsible for running a prompt and returning the result."""

    @abstractmethod
    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        pass  # pragma: no cover


class TextLLMPromptRunner(PromptRunner):
    """A text-based prompt runner is responsible for running a prompt and returning the result."""

    def __init__(self, llm: TextLLM, formatter: PromptFormatter, interceptors: List[PromptInterceptor] = []):
        """Initialize a TextBasedPromptRunner.

        Args:
            llm: The LLM to use. It must be an instance of TextBasedLLM.
            formatter: The prompt formatter to use. It must be an instance of PromptFormatter.
        """
        self.text_llm = llm
        self.formatter = formatter
        self.interceptors = interceptors

    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        """Run the given prompt and return the result.

        Args:
            prompt: The prompt to run. It must be an instance of Prompt.
            input_value: The input value to use. It must be an instance of Value, which is a dict.
        """

        for interceptor in self.interceptors:
            input_value = interceptor.before_run(prompt, input_value)

        raw_req = self.formatter.format_prompt(prompt, input_value)
        raw_resp = self.text_llm.generate(raw_req)
        resp = self.formatter.parse(prompt, raw_resp)

        for interceptor in reversed(self.interceptors):
            resp = interceptor.after_run(prompt, resp)

        return resp
