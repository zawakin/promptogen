from __future__ import annotations

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, ParameterInfo, Prompt, create_sample_prompt
from promptgen.prompt_collection.prompts.python_code_generator import get_python_code_generator_prompt
from promptgen.prompt_collection.prompts.text_categorizer import get_text_categorizer_template


class PromptCreatorInput(DataClass):
    description: str
    background: str


class PromptCreatorOutput(DataClass):
    prompt: Prompt


def get_prompt_creator_template() -> Prompt:
    categorization_prompt = get_text_categorizer_template()
    python_code_generator_prompt = get_python_code_generator_prompt()

    return Prompt(
        name="PromptCreator",
        description="Create a prompt from the given description and background. Use the given description as the prompt description as is. Consider background information to make the prompt more specific.",
        input_parameters=[
            ParameterInfo(
                name="description",
                description="description of the prompt; this will be used as the prompt description as is",
            ),
            ParameterInfo(name="background", description="background of the prompt"),
        ],
        output_parameters=[
            ParameterInfo(
                name="prompt",
                description="A prompt which has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.",
            ),
        ],
        template=Example(
            input=PromptCreatorInput(
                description="description of sample prompt",
                background="background of the prompt",
            ).to_dict(),
            output=PromptCreatorOutput(
                prompt=create_sample_prompt("new prompt"),
            ).to_dict(),
        ),
        examples=[
            Example(
                input=PromptCreatorInput(
                    description=categorization_prompt.description,
                    background="The given text may be a sentence, a paragraph, or a document.",
                ).to_dict(),
                output=PromptCreatorOutput(
                    prompt=categorization_prompt.update(examples=[categorization_prompt.examples[0]]),
                ).to_dict(),
            ),
            Example(
                input=PromptCreatorInput(
                    description=python_code_generator_prompt.description,
                    background="style: input: (task: str), output: (reason: str, code: str)",
                ).to_dict(),
                output=PromptCreatorOutput(
                    prompt=python_code_generator_prompt.update(examples=[python_code_generator_prompt.examples[0]]),
                ).to_dict(),
            ),
        ],
    )
