from __future__ import annotations

from promptgen.dataclass import DataClass
from promptgen.prompt import Example, ParameterInfo, Prompt, create_sample_prompt


class ExtractPromptInput(DataClass):
    raw_text: str


class ExtractPromptOutput(DataClass):
    extracted_prompt: Prompt


def get_prompt_extractor_template() -> Prompt:
    return Prompt.from_dict(
        {
            "name": "PromptExtractor",
            "description": "You are an advanced AI assistant and your goal is to Extract a given prompt from raw text.",
            "input_parameters": [{"name": "raw_text", "description": "raw text in which the prompt is hidden"}],
            "output_parameters": [
                {"name": "extracted_prompt", "description": "Extracted prompt from the given raw text"}
            ],
            "template": {
                "input": {"raw_text": "raw text in which the prompt is hidden"},
                "output": {
                    "extracted_prompt": {
                        "name": "sample-Extracted prompt",
                        "description": "A sample prompt.",
                        "input_parameters": [
                            {"name": "input1", "description": "The first input parameter."},
                            {"name": "input2", "description": "The second input parameter."},
                        ],
                        "output_parameters": [
                            {"name": "output1", "description": "The first output parameter."},
                            {"name": "output2", "description": "The second output parameter."},
                        ],
                        "template": {
                            "input": {"input1": "Hello, world!", "input2": "Hello, world!"},
                            "output": {"output1": "Hello, world!", "output2": "Hello, world!"},
                        },
                        "examples": [
                            {
                                "input": {"input1": "Hello, world!", "input2": "Hello, world!"},
                                "output": {"output1": "Hello, world!", "output2": "Hello, world!"},
                            },
                            {
                                "input": {"input1": "Hello, world!", "input2": "Hello, world!"},
                                "output": {"output1": "Hello, world!", "output2": "Hello, world!"},
                            },
                        ],
                    }
                },
            },
            "examples": [
                {
                    "input": {
                        "raw_text": "Can you help me create a function that calculates the factorial of a number?"
                    },
                    "output": {
                        "extracted_prompt": {
                            "name": "Function for Factorial",
                            "description": "Create a function to calculate the factorial of a given number.",
                            "input_parameters": [
                                {
                                    "name": "number",
                                    "description": "The number for which the factorial needs to be calculated",
                                }
                            ],
                            "output_parameters": [
                                {"name": "factorial", "description": "The factorial of the given number"}
                            ],
                            "template": {"input": {"number": 1}, "output": {"factorial": 1}},
                            "examples": [
                                {"input": {"number": 5}, "output": {"factorial": 120}},
                                {"input": {"number": 3}, "output": {"factorial": 6}},
                            ],
                        }
                    },
                },
                {
                    "input": {"raw_text": "I need to find out how many days are left until Christmas this year."},
                    "output": {
                        "extracted_prompt": {
                            "name": "DaysUntilChristmas",
                            "description": "Calculate the number of days left until Christmas in the current year.",
                            "input_parameters": [{"name": "current_date", "description": "The current date"}],
                            "output_parameters": [
                                {"name": "days_left", "description": "The number of days left until Christmas"}
                            ],
                            "template": {"input": {"current_date": "2000-12-24"}, "output": {"days_left": 1}},
                            "examples": [
                                {"input": {"current_date": "2021-10-01"}, "output": {"days_left": 85}},
                                {"input": {"current_date": "2021-12-01"}, "output": {"days_left": 24}},
                            ],
                        }
                    },
                },
            ],
        }
    )
