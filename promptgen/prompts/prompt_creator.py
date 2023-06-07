from __future__ import annotations

from promptgen.input import InputValue
from promptgen.output import OutputValue
from promptgen.prompt import Example, ParameterInfo, Prompt, create_sample_prompt
from promptgen.prompts.text_categorizer import get_text_categorizer_template
from promptgen.prompts.text_summarizer import get_text_summarizer_template


class PromptCreatorInput(InputValue):
    purpose: str
    background: str


class PromptCreatorOutput(OutputValue):
    prompt: Prompt


def get_prompt_creator_template() -> Prompt:
    categorization_prompt = get_text_categorizer_template()
    summarization_prompt = get_text_summarizer_template()

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
            ),
            output=PromptCreatorOutput(
                prompt=create_sample_prompt("new prompt"),
            ),
        ),
        examples=[
            Example(
                input=PromptCreatorInput(
                    purpose="Categorize the given text into one of the given categories.",
                    background="The given text may be a sentence, a paragraph, or a document.",
                ),
                output=PromptCreatorOutput(
                    prompt=categorization_prompt.with_examples([categorization_prompt.examples[0]]),
                ),
            ),
            Example(
                input=PromptCreatorInput(
                    purpose="Summarize the given text.",
                    background="The given text may be the part of the document.",
                ),
                output=PromptCreatorOutput(
                    prompt=summarization_prompt.with_examples([summarization_prompt.examples[0]]),
                ),
            ),
        ],
    )
