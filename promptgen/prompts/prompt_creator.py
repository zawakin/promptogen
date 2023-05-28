from promptgen.dataclass import DataClass
from promptgen.prompt import Example, ParameterInfo, Prompt
from promptgen.prompts.text_categorizer import get_text_categorizer_template
from promptgen.prompts.text_summarizer import get_text_summarizer_template


class PromptCreatorInput(DataClass):
    purpose: str
    background: str


class PromptCreatorOutput(DataClass):
    prompt: Prompt


def get_prompt_creator_template() -> Prompt:
    categorization_prompt = get_text_categorizer_template()
    summarization_prompt = get_text_summarizer_template()

    return Prompt(
        name="PromptCreator",
        description="Create a prompt from the given purpose. Don't create an example with the input purpose. Instead, create an example with a different purpose. Consider background information that is necessary to understand the purpose.",
        input_parameters={
            "purpose": ParameterInfo(description="purpose of the prompt"),
            "background": ParameterInfo(
                description="background of the prompt"
            ),
        },
        output_parameters={
            "prompt": ParameterInfo(
                description="prompt created from the given purpose. Is has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.",
            ),
        },
        template=Example(
            input=PromptCreatorInput(
                purpose="purpose of the prompt",
                background="background of the prompt",
            ).dict(),
            output=PromptCreatorOutput(
                prompt=Prompt(
                    name="new prompt name",
                    description="new prompt description",
                    input_parameters={
                        "input_1": ParameterInfo(description="input 1"),
                        },
                    output_parameters={
                        "output_1": ParameterInfo(description="output 1"),
                        },
                    template=Example(
                        input=dict(input_1="prompt input 1"),
                        output=dict(output_1="prompt output 1"),
                    ),
                    examples=[],
                ),
            ).dict(),
        ),
        examples=[
            Example(
                input=PromptCreatorInput(
                    purpose="Categorize the given text into one of the given categories.",
                    background="The given text may be a sentence, a paragraph, or a document.",
                ).dict(),
                output=PromptCreatorOutput(
                    prompt=categorization_prompt.with_examples([]),
                ).dict(),
            ),
            Example(
                input=PromptCreatorInput(
                    purpose="Summarize the given text.",
                    background="The given text may be the part of the document.",
                ).dict(),
                output=PromptCreatorOutput(
                    prompt=summarization_prompt.with_examples([]),
                ).dict(),
            ),
        ],
    )
