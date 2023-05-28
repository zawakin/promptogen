from promptgen.dataclass import DataClass
from promptgen.prompt import Example, ParameterInfo, Prompt


class OptimizePromptInput(DataClass):
    original_prompt: Prompt
    background: str


class OptimizePromptOutput(DataClass):
    optimized_prompt: Prompt


def get_prompt_optimizer_template() -> Prompt:
    return Prompt(
        name="PromptOptimizer",
        description="You are an advanced AI assistant and your goal is to optimize a given prompt. You need to focus on improving the prompt title, description, and the number and description of input parameters. You may feel free to add or change any input or output parameters that are necessary to express the purpose of the prompt.",
        input_parameters={
            "original_prompt": ParameterInfo(description="original prompt"),
            "background": ParameterInfo(description="background of the prompt"),
        },
        output_parameters={
            "optimized_prompt": ParameterInfo(description="optimized prompt"),
        },
        template=Example(
            input=OptimizePromptInput(
                original_prompt=Prompt(
                    name="prompt name",
                    description="prompt description",
                    input_parameters={
                        "input_1": ParameterInfo(description="description of input 1"),
                    },
                    output_parameters={
                        "output_1": ParameterInfo(
                            description="description of output 1"
                        ),
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
                background="background of the prompt",
            ).dict(),
            output=OptimizePromptOutput(
                optimized_prompt=Prompt(
                    name="optimized prompt name",
                    description="optimized prompt description",
                    input_parameters={
                        "optimized_input_1": ParameterInfo(
                            description="description of optimized input 1"
                        ),
                        "optimized_input_2": ParameterInfo(
                            description="description of optimized input 2"
                        ),
                    },
                    output_parameters={
                        "optimized_output_1": ParameterInfo(
                            description="description of optimized output 1"
                        ),
                        "optimized_output_2": ParameterInfo(
                            description="description of optimized output 2"
                        ),
                    },
                    template=Example(
                        input={
                            "optimized_input_1": "optimized prompt input 1",
                            "optimized_input_2": "optimized prompt input 2",
                        },
                        output={
                            "optimized_output_1": "optimized prompt output 1",
                            "optimized_output_2": "optimized prompt output 2",
                        },
                    ),
                    examples=[
                        Example(
                            input={
                                "optimized_input_1": "optimized prompt "
                                + "example input 1",
                                "optimized_input_2": "optimized prompt "
                                + "example input 2",
                            },
                            output={
                                "optimized_output_1": "optimized prompt "
                                + "example output 1",
                                "optimized_output_2": "optimized prompt "
                                + "example output 2",
                            },
                        ),
                        Example(
                            input={
                                "optimized_input_1": "optimized prompt "
                                + "example input 3",
                                "optimized_input_2": "optimized prompt "
                                + "example input 4",
                            },
                            output={
                                "optimized_output_1": "optimized prompt "
                                + "example output 3",
                                "optimized_output_2": "optimized prompt "
                                + "example output 4",
                            },
                        ),
                    ],
                ),
            ).dict(),
        ),
        examples=[],
    )
