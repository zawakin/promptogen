from abc import ABC, abstractmethod

from promptogen.model.dataclass import DataClass
from promptogen.model.llm import TextLLM
from promptogen.model.prompt import IOExample, ParameterInfo, Prompt
from promptogen.model.prompt_runner import PromptRunner, TextLLMPromptRunner
from promptogen.model.prompt_transformer import PromptTransformer
from promptogen.model.reasoning_extractor import ExampleReasoning, ReasoningExtractor
from promptogen.model.value_formatter import Value
from promptogen.prompt_collection.prompts.dict_translator import DictTranslatorPrompt
from promptogen.prompt_formatter.json_formatter import JsonPromptFormatter
from promptogen.prompt_formatter.key_value_formatter import KeyValueFormatter, KeyValuePromptFormatter
from promptogen.prompt_formatter.prompt_formatter import PromptFormatter, PromptFormatterConfig
from promptogen.prompt_formatter.text_formatter import TextValueFormatter


class ValueTranslator:
    """Reasoning extractor that uses a text-based LLM."""

    text_llm: TextLLM

    def __init__(
        self,
        *,
        llm: TextLLM,
    ):
        self.text_llm = llm

    def translate_value(self, value: Value, to_lang: str) -> Value:
        translator_prompt = DictTranslatorPrompt()

        formatter = JsonPromptFormatter()

        prompt_runner = TextLLMPromptRunner(
            llm=self.text_llm,
            formatter=formatter,
        )

        resp = prompt_runner.run_prompt(
            translator_prompt,
            input_value={
                "value": value,
                "language": to_lang,
            },
        )

        return resp["translated_value"]
