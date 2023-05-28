from promptgen.dataclass import DataClass
from promptgen.prompt import Example, ParameterInfo, Prompt
from promptgen.prompts.text_categorizer import get_text_categorizer_template
from promptgen.prompts.text_summarizer import get_text_summarizer_template



class ExampleCreatorInput(DataClass):
    prompt: Prompt
    n: int


class ExampleCreatorOutput(DataClass):
    examples: list[Example]


def get_example_creator_template() -> Prompt:
    categorization_prompt = get_text_categorizer_template()
    summarization_prompt = get_text_summarizer_template()

    return Prompt(
        name="PromptExampleCreator",
        description="Create an random-like example from the given prompt. Please add examples with scattered inputs and outputs in semantic space.",
        input_parameters={
            "prompt": ParameterInfo( description="prompt"),
            "n": ParameterInfo(description="number of examples to create"),
            },
        output_parameters={
            "examples": ParameterInfo(
                description="detailed examples of the prompt. Please add examples with scattered inputs and outputs in semantic space. Specific examples are better than general examples.",
            ),
            },
        template=Example(
            input=ExampleCreatorInput(
                prompt=Prompt(
                    name="prompt name",
                    description="prompt description",
                    input_parameters={
                        "input_1": ParameterInfo(description="input 1"),
                        },
                    output_parameters={
                        "output_1": ParameterInfo(description="output 1"),
                        },
                    template=Example(
                        input={
                            "input_1": "prompt input 1",
                        },
                        output={
                            "output_1": "prompt output 1",
                        },
                    ),
                    examples=[
                        Example(
                            input={
                                "input_1": "prompt example input 1",
                            },
                            output={
                                "output_1": "prompt example output 1",
                            },
                        ),
                    ],
                ),
                n=2,
            ).dict(),
            output=ExampleCreatorOutput(
                examples=[
                    Example(
                        input={
                            "input_1": "example input 1",
                        },
                        output={
                            "output_1": "example output 1",
                        },
                    ),
                    Example(
                        input={
                            "input_1": "example input 2",
                        },
                        output={
                            "output_1": "example output 2",
                        },
                    ),
                ],
            ).dict(),
        ),
        examples=[
            Example(
                input=ExampleCreatorInput(
                    prompt=categorization_prompt.with_examples([]),
                    n=2,
                ).dict(),
                output=ExampleCreatorOutput(
                    examples=[
                        categorization_prompt.examples[0],
                        categorization_prompt.examples[1],
                    ],
                ).dict(),
            ),
            Example(
                input=ExampleCreatorInput(
                    prompt=summarization_prompt.with_examples([]),
                    n=2,
                ).dict(),
                output=ExampleCreatorOutput(
                    examples=[
                        summarization_prompt.examples[0],
                        summarization_prompt.examples[1],
                    ],
                ).dict(),
            ),
        ],
    )
