from __future__ import annotations

from typing import List

from promptgen.model.dataclass import DataClass
from promptgen.model.prompt import Example, ParameterInfo, Prompt


class PythonCodeGeneratorPrompt(Prompt):
    name: str = "PythonCodeGenerator"
    description: str = "Generate Python code based on the given task"
    input_parameters: List[ParameterInfo] = [
        ParameterInfo(name="task", description="The task for which Python code needs to be generated")
    ]
    output_parameters: List[ParameterInfo] = [
        ParameterInfo(name="reason", description="Reason for the generated Python code"),
        ParameterInfo(name="code", description="Python code generated to complete the task"),
    ]
    template: Example = Example(
        input={
            "task": "task",
        },
        output={
            "reason": "reason",
            "code": "code",
        },
    )
    examples: List[Example] = [
        Example(
            input={
                "task": "Create a function that calculates the factorial of a number",
            },
            output={
                "reason": "Factorial function is a common use case in Python programming",
                "code": """def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)""",
            },
        )
    ]
