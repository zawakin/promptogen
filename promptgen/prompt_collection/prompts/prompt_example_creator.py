from __future__ import annotations

from typing import List

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, ParameterInfo, Prompt, create_sample_prompt
from promptgen.prompt_collection.prompts.python_code_generator import PythonCodeGeneratorPrompt
from promptgen.prompt_collection.prompts.text_categorizer import TextCategorizerPrompt


class ExampleCreatorPrompt(Prompt):
    name: str = "PromptExampleCreator"
    description: str = "Create an random-like example from the given prompt. Please add examples with scattered inputs and outputs in semantic space."
    input_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="prompt",
            description="prompt",
        ),
    ]
    output_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="example",
            description="detailed example of the prompt. Please add an example with scattered inputs and outputs in semantic space. Specific example is better than general examples.",
        ),
    ]
    template: Example = Example(
        input={
            "prompt": create_sample_prompt("prompt"),
        },
        output={
            "example": Example(
                input={
                    "input_1": "example input 1",
                },
                output={
                    "output_1": "example output 1",
                },
            ),
        },
    )
    examples: List[Example] = [
        Example(
            input={
                "prompt": TextCategorizerPrompt(examples=[]),
            },
            output={
                "example": TextCategorizerPrompt().examples[0],
            },
        ),
        Example(
            input={
                "prompt": PythonCodeGeneratorPrompt(examples=[]),
            },
            output={
                "example": PythonCodeGeneratorPrompt().examples[0],
            },
        ),
    ]
