from __future__ import annotations

from typing import List

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, ParameterInfo, Prompt, create_sample_prompt
from promptgen.prompt_collection.prompts.python_code_generator import get_python_code_generator_prompt
from promptgen.prompt_collection.prompts.text_categorizer import get_text_categorizer_template


class ExampleCreatorInput(DataClass):
    prompt: Prompt


class ExampleCreatorOutput(DataClass):
    example: Example


def get_example_creator_template() -> Prompt:
    categorization_prompt = get_text_categorizer_template()
    python_code_generator_prompt = get_python_code_generator_prompt()

    return Prompt(
        name="PromptExampleCreator",
        description="Create an random-like example from the given prompt. Please add examples with scattered inputs and outputs in semantic space.",
        input_parameters=[
            ParameterInfo(name="prompt", description="prompt"),
        ],
        output_parameters=[
            ParameterInfo(
                name="example",
                description="detailed example of the prompt. Please add an example with scattered inputs and outputs in semantic space. Specific example is better than general examples.",
            ),
        ],
        template=Example(
            input=ExampleCreatorInput(
                prompt=create_sample_prompt("prompt"),
            ).model_dump(),
            output=ExampleCreatorOutput(
                example=Example(
                    input={
                        "input_1": "example input 1",
                    },
                    output={
                        "output_1": "example output 1",
                    },
                ),
            ).model_dump(),
        ),
        examples=[
            Example(
                input=ExampleCreatorInput(
                    prompt=categorization_prompt.with_examples([]),
                ).model_dump(),
                output=ExampleCreatorOutput(
                    example=categorization_prompt.examples[0],
                ).model_dump(),
            ),
            Example(
                input=ExampleCreatorInput(
                    prompt=python_code_generator_prompt.with_examples([]),
                ).model_dump(),
                output=ExampleCreatorOutput(
                    example=python_code_generator_prompt.examples[0],
                ).model_dump(),
            ),
        ],
    )
