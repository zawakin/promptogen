from __future__ import annotations

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, ParameterInfo, Prompt, create_sample_prompt
from promptgen.prompt_collection.prompts.python_code_generator import get_python_code_generator_prompt
from promptgen.prompt_collection.prompts.text_categorizer import get_text_categorizer_template


class PromptCreatorInput(DataClass):
    purpose: str
    background: str


class PromptCreatorOutput(DataClass):
    prompt: Prompt


def get_prompt_creator_template() -> Prompt:
    categorization_prompt = get_text_categorizer_template()
    python_code_generator_prompt = get_python_code_generator_prompt()

    return Prompt(
        name="PromptCreator",
        description="Create a prompt from the given purpose. Don't create an example with the input purpose. Instead, create an example with a different purpose. Consider background information that is necessary to understand the purpose.",
        input_parameters=[
            ParameterInfo(name="purpose", description="purpose of the prompt"),
            ParameterInfo(name="background", description="background of the prompt"),
        ],
        output_parameters=[
            ParameterInfo(
                name="prompt",
                description="prompt created from the given purpose. Is has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.",
            ),
        ],
        template=Example(
            input=PromptCreatorInput(
                purpose="purpose of the prompt",
                background="background of the prompt",
            ).dict(),
            output=PromptCreatorOutput(
                prompt=create_sample_prompt("new prompt"),
            ).dict(),
        ),
        examples=[
            Example(
                input=PromptCreatorInput(
                    purpose="Categorize the given text into one of the given categories.",
                    background="The given text may be a sentence, a paragraph, or a document.",
                ).dict(),
                output=PromptCreatorOutput(
                    prompt=categorization_prompt.with_examples([categorization_prompt.examples[0]]),
                ).dict(),
            ),
            Example(
                input=PromptCreatorInput(
                    purpose="Python code generator",
                    background="style: input: (task: str), output: (reason: str, code: str)",
                ).dict(),
                output=PromptCreatorOutput(
                    prompt=python_code_generator_prompt.with_examples([python_code_generator_prompt.examples[0]]),
                ).dict(),
            ),
        ],
    )
