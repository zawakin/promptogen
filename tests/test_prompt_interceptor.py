from typing import List, Tuple
from pydantic import BaseModel
import pytest
from promptogen.model.llm import FunctionBasedTextLLM, TextLLM
from promptogen.model.prompt import create_sample_prompt
from promptogen.model.prompt_runner import TextLLMPromptRunner
from promptogen.prompt_collection.prompts.text_summarizer import TextSummarizerPrompt

from promptogen.prompt_formatter import JsonValueFormatter, KeyValueFormatter
from promptogen.prompt_formatter.key_value_formatter import KeyValuePromptFormatter
from promptogen.prompt_interceptor.translation_interceptor import ValueTranslationInterceptor


def test_value_translation_interceptor_before_run():
    prompt = TextSummarizerPrompt()

    def llm_func(s: str) -> str:
        if "input text" in s:
            return """```json
    {
        "translated_value": {
            "text": "translated text"
        }
    }
    ```"""
        if "output text" in s:
            return """```json
    {
        "translated_value": {
            "summary": "translated text"
        }
    }
    ```"""
        raise Exception(f"Unexpected input: {s}")

    llm: TextLLM = FunctionBasedTextLLM(llm_func)
    interceptor = ValueTranslationInterceptor(llm=llm, from_lang="Japanese", to_lang="English")
    resp = interceptor.before_run(prompt, {
        'text': 'input text',
    })
    assert resp['text'] == 'translated text'

    resp = interceptor.after_run(prompt, {
        'summary': 'output text',
    })
    assert resp['summary'] == 'translated text'
