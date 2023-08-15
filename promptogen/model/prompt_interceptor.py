from abc import ABC, abstractmethod
from typing import Callable

from promptogen.model.llm import TextLLM
from promptogen.model.prompt import Prompt
from promptogen.model.value_formatter import Value
from promptogen.prompt_formatter.prompt_formatter import PromptFormatter


class PromptInterceptor(ABC):
    """An interceptor for the PromptRunner."""

    @abstractmethod
    def before_run(self, prompt: Prompt, input_value: Value) -> Value:
        """Process before running the prompt. Can modify the input_value."""
        pass

    @abstractmethod
    def after_run(self, prompt: Prompt, output_value: Value) -> Value:
        """Process after running the prompt. Can modify the output_value."""
        pass


class LoggingInterceptor(PromptInterceptor):
    def before_run(self, _: Prompt, input_value: Value) -> Value:
        print(f"Running prompt with input: {input_value}")
        return input_value

    def after_run(self, _: Prompt, output_value: Value) -> Value:
        print(f"Prompt produced output: {output_value}")
        return output_value
