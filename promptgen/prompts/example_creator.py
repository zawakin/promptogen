from promptgen.dataclass import DataClass
from promptgen.prompt import Prompt, ParameterInfo, Example

from .categorization import Categorization
from .summarization import Summarization


class ExampleCreatorInput(DataClass):
    prompt: Prompt
    n: int


class ExampleCreatorOutput(DataClass):
    examples: list[Example]


class ExampleCreator(Prompt):
    def __init__(self):
        categorization_prompt = Categorization()
        summarization_prompt = Summarization()

        super().__init__(
            name="example_creator",
            description="Create an random-like example from the given prompt. Please add examples with scattered inputs and outputs in semantic space.",
            input_parameters=[
                ParameterInfo(name="prompt", description="prompt"),
                ParameterInfo(name="n", description="number of examples to create"),
            ],
            output_parameters=[
                ParameterInfo(
                    name="examples",
                    description="detailed examples of the prompt. Please add examples with scattered inputs and outputs in semantic space. Specific examples are better than general examples.",
                ),
            ],
            template=Example(
                input=ExampleCreatorInput(
                    prompt=Prompt(
                        name="prompt name",
                        description="prompt description",
                        input_parameters=[
                            ParameterInfo(name="input_1", description="input 1"),
                        ],
                        output_parameters=[
                            ParameterInfo(name="output_1", description="output 1"),
                        ],
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
                        prompt=categorization_prompt.copy(deep=True),
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
                        prompt=summarization_prompt.copy(deep=True),
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
