from typing import List, Tuple
from pydantic import BaseModel
import pytest
from promptgen.model.llm import FunctionBasedTextLLM
from promptgen.model.prompt_runner import TextLLMPromptRunner
from promptgen.prompt_collection.prompts.text_summarizer import TextSummarizerPrompt

from promptgen.prompt_formatter import JsonValueFormatter, KeyValueFormatter
from promptgen.prompt_formatter.key_value_formatter import KeyValuePromptFormatter


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
    formatter = KeyValuePromptFormatter()
    llm = FunctionBasedTextLLM(lambda _: 'summary: sample response returned by the LLM')
    prompt_runner = TextLLMPromptRunner(llm=llm, formatter=formatter)

    resp = prompt_runner.run_prompt(prompt, {
        'text': "This is a sample text to summarize.",
    })

    assert resp['summary'] == 'sample response returned by the LLM'
