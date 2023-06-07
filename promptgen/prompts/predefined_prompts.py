from __future__ import annotations

from typing import List

from promptgen.prompt import Prompt
from .prompt_creator import get_prompt_creator_template
from .prompt_example_creator import get_example_creator_template
from .prompt_optimizer import get_prompt_optimizer_template
from .python_code_generator import get_python_code_generator_prompt
from .text_categorizer import get_text_categorizer_template
from .text_summarizer import get_text_summarizer_template
from .python_code_generator import get_python_code_generator_prompt


def load_predefined_prompts() -> List[Prompt]:
    prompts = [
        get_text_categorizer_template(),
        get_text_summarizer_template(),
        get_example_creator_template(),
        get_prompt_creator_template(),
        get_prompt_optimizer_template(),
        get_python_code_generator_prompt(),
    ]

    return prompts
