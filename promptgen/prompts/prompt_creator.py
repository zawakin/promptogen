from promptgen.dataclass import DataClass
from promptgen.prompt import Prompt, ParameterInfo, Example

from .categorization import Categorization
from .summarization import Summarization


class PromptCreatorInput(DataClass):
    purpose: str
    background: str


class PromptCreatorOutput(DataClass):
    prompt: Prompt


class PromptCreator(Prompt):
    def __init__(self):
        categorization_prompt = Categorization()
        summarization_prompt = Summarization()

        super().__init__(
            name="PromptCreator",
            description="Create a prompt from the given purpose. Don't create an example with the input purpose. Instead, create an example with a different purpose. Consider background information that is necessary to understand the purpose.",
            input_parameters=[
                ParameterInfo(name="purpose",
                              description="purpose of the prompt"),
                ParameterInfo(name="background",
                              description="background of the prompt"),
            ],
            output_parameters=[
                ParameterInfo(
                    name="prompt", description="prompt created from the given purpose. Is has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'."),
            ],
            template=Example(
                input=PromptCreatorInput(
                    purpose="purpose of the prompt",
                    background="background of the prompt",
                ).dict(),
                output=PromptCreatorOutput(
                    prompt=Prompt(
                        name="new prompt name",
                        description="new prompt description",
                        input_parameters=[
                            ParameterInfo(name="input_1",
                                          description="input 1"),
                        ],
                        output_parameters=[
                            ParameterInfo(name="output_1",
                                          description="output 1"),
                        ],
                        template=Example(
                            input=dict(input_1="prompt input 1"),
                            output=dict(output_1="prompt output 1"),
                        ),
                        examples=[
                            Example(
                                input=dict(input_1="prompt example input 1"),
                                output=dict(
                                    output_1="prompt example output 1"),
                            ),
                        ],
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
                        prompt=categorization_prompt,
                    ).dict(),
                ),
                Example(
                    input=PromptCreatorInput(
                        purpose="Summarize the given text.",
                        background="The given text may be the part of the document.",
                    ).dict(),
                    output=PromptCreatorOutput(
                        prompt=summarization_prompt,
                    ).dict(),
                ),
            ],
        )
