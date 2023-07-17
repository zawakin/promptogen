from __future__ import annotations

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, ParameterInfo, Prompt, create_sample_prompt


class OptimizePromptInput(DataClass):
    original_prompt: Prompt
    background: str


class OptimizePromptOutput(DataClass):
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
            input=OptimizePromptInput(
                original_prompt=create_sample_prompt("original prompt"),
                background="background of the prompt",
            ).dict(),
            output=OptimizePromptOutput(
                optimized_prompt=create_sample_prompt("optimized prompt"),
            ).dict(),
        ),
        examples=[],
    )
