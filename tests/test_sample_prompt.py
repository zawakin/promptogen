from promptgen.prompt import Prompt, load_prompt_from_json_file
from promptgen.prompts.text_categorizer import TextCategorizer
from promptgen.prompts.prompt_example_creator import PromptExampleCreator
from promptgen.prompts.prompt_creator import PromptCreator
from promptgen.prompts.prompt_optimizer import PromptOptimizer
from promptgen.prompts.text_summarizer import TextSummarizer


def test_load_prompts():
    prompts = [
        TextSummarizer(),
        TextCategorizer(),
        PromptExampleCreator(),
        PromptCreator(),
        PromptOptimizer(),
    ]

    for prompt in prompts:
        assert isinstance(prompt, Prompt)


def test_load_prompts_from_json_file():
    import os

    prompts_dir = "tests/fixtures/prompts"
    prompts = []

    for filename in os.listdir(prompts_dir):
        prompts.append(load_prompt_from_json_file(
            os.path.join(prompts_dir, filename)))

    for prompt in prompts:
        assert isinstance(prompt, Prompt)
