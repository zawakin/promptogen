from promptgen.prompt_collection import PromptCollection
from promptgen.prompt import Prompt, load_prompt_from_json_file


def test_collection_prompts():
    collection = PromptCollection()
    prompts = collection.prompts

    for name, prompt in prompts.items():
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
