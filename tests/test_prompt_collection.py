from __future__ import annotations

import pytest

from promptgen.prompt_collection.prompt_collection import PromptCollection
from promptgen.prompt_collection.prompts.text_categorizer import TextCategorizerPrompt
from promptgen.prompt_collection.prompts.text_summarizer import TextSummarizerPrompt


def test_prompt_collection():
    c = PromptCollection()

    assert len(c.prompts) == 0


def test_prompt_collection_load_predefined():
    c = PromptCollection.load_predefined()

    assert len(c.prompts) > 0


def test_prompt_collection_repr__str__():
    c = PromptCollection(prompts={
        'TextSummarizer': TextSummarizerPrompt(),
        'TextCategorizer': TextCategorizerPrompt(),
    })

    assert repr(c) == f"PromptCollection(prompt_names=['TextSummarizer', 'TextCategorizer'])"
    assert str(c) == """
Prompts Overview
----------------
  TextSummarizer: (text: str) -> (summary: str)
  TextCategorizer: (text: str, categories: list) -> (category: str)

Use 'details()' method to view full details of each prompt."""


def test_prompt_collection_details():
    c = PromptCollection(prompts={
        'TextSummarizer': TextSummarizerPrompt(),
        'TextCategorizer': TextCategorizerPrompt(),
    })

    assert c.details() == f"""
Prompts Details
---------------
  TextSummarizer: {c.prompts['TextSummarizer'].description}

  TextCategorizer: {c.prompts['TextCategorizer'].description}
"""
