from __future__ import annotations

from typing import List

from promptogen.model.dataclass import DataClass
from promptogen.model.prompt import IOExample, ParameterInfo, Prompt, create_sample_prompt


class OptimizePromptInput(DataClass):
    original_prompt: Prompt
    background: str


class OptimizePromptOutput(DataClass):
    optimized_prompt: Prompt


class PromptOptimizerPrompt(Prompt):
    name: str = "PromptOptimizer"
    description: str = "You are an advanced AI assistant and your goal is to optimize a given prompt. You need to focus on improving the prompt title, description, and the number and description of input parameters. You may feel free to add or change any input or output parameters that are necessary to express the purpose of the prompt."
    input_parameters: List[ParameterInfo] = [
        ParameterInfo(name="original_prompt", description="original prompt"),
        ParameterInfo(name="background", description="background of the prompt"),
    ]
    output_parameters: List[ParameterInfo] = [
        ParameterInfo(name="optimized_prompt", description="optimized prompt"),
    ]
    template: IOExample = IOExample(
        input={
            "original_prompt": create_sample_prompt("original prompt"),
            "background": "background of the prompt",
        },
        output={
            "optimized_prompt": create_sample_prompt("optimized prompt"),
        },
    )
    examples: List[IOExample] = []
