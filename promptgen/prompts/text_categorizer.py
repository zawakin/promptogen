from __future__ import annotations

from typing import List

from promptgen.dataclass import DataClass
from promptgen.input import InputValue
from promptgen.output import OutputValue
from promptgen.prompt import Example, ParameterInfo, Prompt


class TextCategorzierInput(DataClass):
    text: str
    categories: List[str]


class TextCategorizerOutput(DataClass):
    category: str


def get_text_categorizer_template() -> Prompt:
    return Prompt(
        name="TextCategorizer",
        description="Categorize the given text",
        input_parameters=[
            ParameterInfo(name="text", description="The text to be categorized"),
            ParameterInfo(name="categories", description="The categories to categorize the text into"),
        ],
        output_parameters=[
            ParameterInfo(name="category", description="The category the text belongs to"),
        ],
        template=Example(
            input=TextCategorzierInput(
                text="text",
                categories=["category 1", "category 2"],
            ).dict(),
            output=TextCategorizerOutput(
                category="category 1",
            ).dict(),
        ),
        examples=[
            Example(
                input=TextCategorzierInput(
                    text="A recent study shows that regular exercise can help improve cognitive function in older adults.",
                    categories=["Health", "Science", "Technology"],
                ).dict(),
                output=TextCategorizerOutput(
                    category="Health",
                ).dict(),
            ),
            Example(
                input=TextCategorzierInput(
                    text="The new quantum computing system is expected to revolutionize data processing and complex calculations.",
                    categories=["Health", "Science", "Technology"],
                ).dict(),
                output=TextCategorizerOutput(
                    category="Technology",
                ).dict(),
            ),
        ],
    )
