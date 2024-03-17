from typing import List, Tuple
from pydantic import BaseModel
import pytest
from promptogen.model.llm import FunctionBasedTextLLM, TextLLM
from promptogen.model.prompt import Prompt
from promptogen.model.prompt_interceptor import PromptInterceptor
from promptogen.model.prompt_runner import TextLLMPromptRunner
from promptogen.model.value_formatter import Value
from promptogen.prompt_collection.prompts.text_summarizer import TextSummarizerPrompt

from promptogen.prompt_formatter import JsonValueFormatter, KeyValueFormatter
from promptogen.prompt_formatter.key_value_formatter import KeyValuePromptFormatter
from promptogen.prompt_formatter.prompt_formatter import PromptFormatterInterface
from promptogen.prompt_interceptor.translation_interceptor import ValueTranslationInterceptor


@pytest.fixture
def dataclass():
    class Tmp(BaseModel):
        test_output_parameter_name: str = 'test output parameter value' # type: ignore
        test_output_parameter_name_2: str = 'test output parameter value 2' # type: ignore

    return Tmp()


@pytest.fixture
def output_keys() -> List[Tuple[str, type]]:
    return [
        ('test output parameter name', str),
        ('test output parameter name 2', str)
    ]


def test_llm_prompt_runner_run_prompt():
    prompt = TextSummarizerPrompt()
    formatter: PromptFormatterInterface = KeyValuePromptFormatter()
    llm: TextLLM = FunctionBasedTextLLM(lambda _: 'summary: sample response returned by the LLM')
    prompt_runner = TextLLMPromptRunner(llm=llm, formatter=formatter)

    resp = prompt_runner.run_prompt(prompt, {
        'text': "This is a sample text to summarize.",
    })

    assert resp['summary'] == 'sample response returned by the LLM'


def test_llm_prompt_runner_run_prompt_interceptors():
    prompt = TextSummarizerPrompt()
    formatter = KeyValuePromptFormatter()
    llm: TextLLM = FunctionBasedTextLLM(lambda _: 'summary: sample response returned by the LLM')

    class TestInterceptor(PromptInterceptor):
        def before_run(self, _: Prompt, input_value: Value) -> Value:
            return {
                'text': 'translated text',
            }

        def after_run(self, _: Prompt, output_value: Value) -> Value:
            return {
                'summary': 'translated text',
            }

    prompt_runner = TextLLMPromptRunner(llm=llm, formatter=formatter, interceptors=[TestInterceptor()])

    resp = prompt_runner.run_prompt(prompt, {
        'text': "This is a sample text to summarize.",
    })

    assert resp['summary'] == 'translated text'
