from __future__ import annotations

from typing import List

from promptogen.model.prompt import Prompt

from .prompts import (
    DictTranslatorPrompt,
    ExampleCreatorPrompt,
    PromptCreatorPrompt,
    PromptOptimizerPrompt,
    PythonCodeGeneratorPrompt,
    TextCategorizerPrompt,
    TextCondenserPrompt,
    TextSummarizerPrompt,
)


def load_predefined_prompts() -> List[Prompt]:
    prompts: List[Prompt] = [
        PromptCreatorPrompt(),
        TextCategorizerPrompt(),
        TextSummarizerPrompt(),
        ExampleCreatorPrompt(),
        PromptOptimizerPrompt(),
        PythonCodeGeneratorPrompt(),
        TextCondenserPrompt(),
        DictTranslatorPrompt(),
    ]

    return prompts
