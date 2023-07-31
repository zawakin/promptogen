from __future__ import annotations

import pytest
from promptgen.model.prompt import create_sample_prompt

from promptgen.prompt_collection.prompt_collection import PredefinedPromptCollection, PromptCollection


def test_prompt_collection():
    c = PromptCollection()

    assert len(c.prompts) == 0


def test_prompt_collection_load_predefined():
    c = PredefinedPromptCollection()

    assert len(c.prompts) > 0
