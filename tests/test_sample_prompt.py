from promptogen.prompt import Prompt
from promptogen.prompts.categorization import Categorization
from promptogen.prompts.example_creator import ExampleCreator
from promptogen.prompts.prompt_creator import PromptCreator
from promptogen.prompts.prompt_optimizer import PromptOptimizer
from promptogen.prompts.summarization import Summarization


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
