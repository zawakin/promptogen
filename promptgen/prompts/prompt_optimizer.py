from __future__ import annotations

from promptgen.input import InputValue
from promptgen.output import OutputValue
from promptgen.prompt import Example, ParameterInfo, Prompt, create_sample_prompt


class OptimizePromptInput(InputValue):
    original_prompt: Prompt
    background: str


class OptimizePromptOutput(OutputValue):
    optimized_prompt: Prompt


def get_prompt_optimizer_template() -> Prompt:
    return Prompt(
        name="PromptOptimizer",
        description="You are an advanced AI assistant and your goal is to optimize a given prompt. You need to focus on improving the prompt title, description, and the number and description of input parameters. You may feel free to add or change any input or output parameters that are necessary to express the purpose of the prompt.",
        input_parameters=[
            ParameterInfo(name="original_prompt", description="original prompt"),
            ParameterInfo(name="background", description="background of the prompt"),
        ],
        output_parameters=[
            ParameterInfo(name="optimized_prompt", description="optimized prompt"),
        ],
        template=Example(
            input=InputValue.from_dataclass(
                OptimizePromptInput(
                    original_prompt=create_sample_prompt("original prompt"),
                    background="background of the prompt",
                )
            ),
            output=OutputValue.from_dataclass(
                OptimizePromptOutput(
                    optimized_prompt=create_sample_prompt("optimized prompt"),
                )
            ),
        ),
        examples=[],
    )
