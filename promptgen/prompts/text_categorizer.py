from promptgen.dataclass import DataClass
from promptgen.prompt import Example, ParameterInfo, Prompt


class TextCategorzierInput(DataClass):
    text: str
    categories: list[str]


class TextCategorizerOutput(DataClass):
    category: str
    found: bool


class TextCategorizer(Prompt):
    def __init__(self):
        super().__init__(
            name="TextCategorizer",
            description="Categorize the given text",
            input_parameters={
                "text": ParameterInfo(description="The text to be categorized"),
                "categories": ParameterInfo(
                    description="The categories to categorize the text into",
                ),
                },
            output_parameters={
                "category": ParameterInfo(
                    description="The category the text belongs to"
                ),
                "found": ParameterInfo(
                    description="Whether the category was found in the text",
                ),
                },
            template=Example(
                input=TextCategorzierInput(
                    text="text",
                    categories=["category 1", "category 2"],
                ).dict(),
                output=TextCategorizerOutput(
                    category="category 1",
                    found=True,
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
                        found=True,
                    ).dict(),
                ),
                Example(
                    input=TextCategorzierInput(
                        text="The new quantum computing system is expected to revolutionize data processing and complex calculations.",
                        categories=["Health", "Sports"],
                    ).dict(),
                    output=TextCategorizerOutput(
                        category="",
                        found=False,
                    ).dict(),
                ),
            ],
        )
