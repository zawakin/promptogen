from promptgen.prompt import Prompt, load_prompt_from_json_file
from promptgen.prompts.categorization import Categorization
from promptgen.prompts.example_creator import ExampleCreator
from promptgen.prompts.prompt_creator import PromptCreator
from promptgen.prompts.prompt_optimizer import PromptOptimizer
from promptgen.prompts.summarization import Summarization


def test_load_prompts():
    prompts = [
        Summarization(),
        Categorization(),
        ExampleCreator(),
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
