from __future__ import annotations

from typing import List

from promptogen.model.dataclass import DataClass
from promptogen.model.prompt import IOExample, ParameterInfo, Prompt, create_sample_prompt
from promptogen.prompt_collection.prompts.python_code_generator import PythonCodeGeneratorPrompt
from promptogen.prompt_collection.prompts.text_categorizer import TextCategorizerPrompt


class PromptCreatorPrompt(Prompt):
    name: str = "PromptCreator"
    description: str = "Create a prompt from the given description and background. Use the given description as the prompt description as is. Consider background information to make the prompt more specific."
    input_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="description",
            description="description of the prompt; this will be used as the prompt description as is",
        ),
        ParameterInfo(name="background", description="background of the prompt"),
    ]
    output_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="prompt",
            description="A prompt which has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.",
        ),
    ]
    template: IOExample = IOExample(
        input={
            "description": "description of sample prompt",
            "background": "background of the prompt",
        },
        output={
            "prompt": create_sample_prompt("new prompt"),
        },
    )
    examples: List[IOExample] = [
        IOExample(
            input={
                "description": TextCategorizerPrompt().description,
                "background": "The given text may be a sentence, a paragraph, or a document.",
            },
            output={
                "prompt": TextCategorizerPrompt(examples=[TextCategorizerPrompt().examples[0]]),
            },
        ),
        IOExample(
            input={
                "description": PythonCodeGeneratorPrompt().description,
                "background": "style: input: (task: str), output: (reason: str, code: str)",
            },
            output={
                "prompt": PythonCodeGeneratorPrompt(examples=[PythonCodeGeneratorPrompt().examples[0]]),
            },
        ),
    ]
