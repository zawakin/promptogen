from __future__ import annotations

from typing import List

from promptogen.model.dataclass import DataClass
from promptogen.model.prompt import IOExample, ParameterInfo, Prompt


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
    template: IOExample = IOExample(
        input={
            "task": "task",
        },
        output={
            "reason": "reason",
            "code": "code",
        },
    )
    examples: List[IOExample] = [
        IOExample(
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
