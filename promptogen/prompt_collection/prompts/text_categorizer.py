from __future__ import annotations

from typing import List

from promptogen.model.prompt import IOExample, ParameterInfo, Prompt


class TextCategorizerPrompt(Prompt):
    name: str = "TextCategorizer"
    description: str = "Categorize the given text"
    input_parameters: List[ParameterInfo] = [
        ParameterInfo(name="text", description="The text to be categorized"),
        ParameterInfo(name="categories", description="The categories to categorize the text into"),
    ]
    output_parameters: List[ParameterInfo] = [
        ParameterInfo(name="category", description="The category the text belongs to"),
    ]
    template: IOExample = IOExample(
        input={
            "text": "text",
            "categories": ["category 1", "category 2"],
        },
        output={
            "category": "category 1",
        },
    )
    examples: List[IOExample] = [
        IOExample(
            input={
                "text": "A recent study shows that regular exercise can help improve cognitive function in older adults.",
                "categories": ["Health", "Science", "Technology"],
            },
            output={
                "category": "Health",
            },
        ),
        IOExample(
            input={
                "text": "The new quantum computing system is expected to revolutionize data processing and complex calculations.",
                "categories": ["Health", "Science", "Technology"],
            },
            output={
                "category": "Technology",
            },
        ),
    ]
