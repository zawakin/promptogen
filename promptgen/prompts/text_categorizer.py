from promptgen.dataclass import DataClass
from promptgen.input import InputValue
from promptgen.output import OutputValue
from promptgen.prompt import Example, ParameterInfo, Prompt


class TextCategorzierInput(DataClass):
    text: str
    categories: list[str]


class TextCategorizerOutput(DataClass):
    category: str
    found: bool


def get_text_categorizer_template() -> Prompt:
    return Prompt(
        name="TextCategorizer",
        description="Categorize the given text",
        input_parameters={
            "text": ParameterInfo(description="The text to be categorized"),
            "categories": ParameterInfo(
                description="The categories to categorize the text into",
            ),
        },
        output_parameters={
            "category": ParameterInfo(description="The category the text belongs to"),
            "found": ParameterInfo(
                description="Whether the category was found in the text",
            ),
        },
        template=Example(
            input=InputValue.from_dataclass(
                TextCategorzierInput(
                    text="text",
                    categories=["category 1", "category 2"],
                )
            ),
            output=OutputValue.from_dataclass(
                TextCategorizerOutput(
                    category="category 1",
                    found=True,
                )
            ),
        ),
        examples=[
            Example(
                input=InputValue.from_dataclass(
                    TextCategorzierInput(
                        text="A recent study shows that regular exercise can help improve cognitive function in older adults.",
                        categories=["Health", "Science", "Technology"],
                    )
                ),
                output=OutputValue.from_dataclass(
                    TextCategorizerOutput(
                        category="Health",
                        found=True,
                    )
                ),
            ),
            Example(
                input=InputValue.from_dataclass(
                    TextCategorzierInput(
                        text="The new quantum computing system is expected to revolutionize data processing and complex calculations.",
                        categories=["Health", "Sports"],
                    )
                ),
                output=OutputValue.from_dataclass(
                    TextCategorizerOutput(
                        category="",
                        found=False,
                    )
                ),
            ),
        ],
    )
