from __future__ import annotations

from promptgen.input import InputValue
from promptgen.output import OutputValue
from promptgen.prompt import Example, ParameterInfo, Prompt


class PythonCodeGeneratorInput(InputValue):
    task: str


class PythonCodeGeneratorOutput(OutputValue):
    reason: str
    code: str


def get_python_code_generator_prompt() -> Prompt:
    return Prompt.from_dict({
    "name": "PythonCodeGenerator",
    "description": "Generate Python code based on the given task",
    "input_parameters": [
        {
            "name": "task",
            "description": "The task for which Python code needs to be generated"
        }
    ],
    "output_parameters": [
        {
            "name": "reason",
            "description": "Reason for the generated Python code"
        },
        {
            "name": "code",
            "description": "Python code generated to complete the task"
        }
    ],
    "template": {
        "input": {
            "task": "task"
        },
        "output": {
            "reason": "reason",
            "code": "code"
        }
    },
    "examples": [
        {
            "input": {
                "task": "Create a function that calculates the factorial of a number"
            },
            "output": {
                "reason": "Factorial function is a common use case in Python programming",
                "code": """def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)"""
            }
        }
    ]
})
