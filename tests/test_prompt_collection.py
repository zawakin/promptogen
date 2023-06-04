from __future__ import annotations

import pytest
from promptgen.prompt import create_sample_prompt

from promptgen.prompt_collection.prompt_collection import PromptCollection


def test_prompt_collection_load_predefined():
    c1 = PromptCollection(load_predefined=True)

    assert len(c1) > 0


def test_prompt_collection_add_prompt():
    c = PromptCollection(load_predefined=False)

    assert len(c) == 0
    c.add_prompt(create_sample_prompt("prompt"))
    assert len(c) == 1


def test_prompt_collection_add_prompt_not_prompt():
    c = PromptCollection(load_predefined=False)

    with pytest.raises(Exception):
        c.add_prompt("not_prompt") # type: ignore


def test_prompt_collection_get_prompt():
    c = PromptCollection(load_predefined=False)
    p = create_sample_prompt("prompt")
    c.add_prompt(p)

    assert c.get_prompt(p.name) == p


def test_prompt_collection_get_prompt_not_found():
    c = PromptCollection(load_predefined=False)
    p = create_sample_prompt("prompt")
    c.add_prompt(p)

    with pytest.raises(Exception):
        c.get_prompt("not_found")


def test_prompt_collection_list_prompts():
    c = PromptCollection(load_predefined=False)
    p = create_sample_prompt("prompt")
    c.add_prompt(p)

    assert c.list_prompts() == [p.name]


def test_prompt_collection_dict():
    c = PromptCollection(load_predefined=False)
    p = create_sample_prompt("prompt")
    c.add_prompt(p)

    assert c[p.name] == p

    s = create_sample_prompt("prompt2")
    c[s.name] = s
    assert c[p.name] == p
    assert c[s.name] == s
    assert p.name in c

    del c[p.name]

    assert s.name in c
    assert p.name not in c


def test_prompt_collection_str():
    c = PromptCollection(load_predefined=False)
    ps = [create_sample_prompt("prompt"), create_sample_prompt("prompt2")]
    c.add_prompt(ps[0])
    c.add_prompt(ps[1])

    assert str(c) == f"""Available prompts:
- {ps[0].name}: {ps[0].description}
- {ps[1].name}: {ps[1].description}
"""


def test_prompt_collection_repr():
    c = PromptCollection(load_predefined=False)
    ps = [create_sample_prompt("prompt"), create_sample_prompt("prompt2")]
    c.add_prompt(ps[0])
    c.add_prompt(ps[1])

    assert repr(c) == f"""Available prompts:
- {ps[0].name}: {ps[0].description}
- {ps[1].name}: {ps[1].description}
"""
