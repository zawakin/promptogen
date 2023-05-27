from promptgen.dataclass import DataClass
from promptgen.prompt import Prompt, ParameterInfo, Example


class CategorizationInput(DataClass):
    text: str
    categories: list[str]


class CategorizationOutput(DataClass):
    category: str
    found: bool


class Categorization(Prompt):
    def __init__(self):
        super().__init__(
            name="Categorization",
            description="Categorize the given text",
            input_parameters=[
                ParameterInfo(name="text", description="The text to be categorized"),
                ParameterInfo(
                    name="categories",
                    description="The categories to categorize the text into",
                ),
            ],
            output_parameters=[
                ParameterInfo(
                    name="category", description="The category the text belongs to"
                ),
                ParameterInfo(
                    name="found",
                    description="Whether the category was found in the text",
                ),
            ],
            template=Example(
                input=CategorizationInput(
                    text="text",
                    categories=["category 1", "category 2"],
                ).dict(),
                output=CategorizationOutput(
                    category="category 1",
                    found=True,
                ).dict(),
            ),
            examples=[
                Example(
                    input=CategorizationInput(
                        text="A recent study shows that regular exercise can help improve cognitive function in older adults.",
                        categories=["Health", "Science", "Technology"],
                    ).dict(),
                    output=CategorizationOutput(
                        category="Health",
                        found=True,
                    ).dict(),
                ),
                Example(
                    input=CategorizationInput(
                        text="The new quantum computing system is expected to revolutionize data processing and complex calculations.",
                        categories=["Health", "Sports"],
                    ).dict(),
                    output=CategorizationOutput(
                        category="",
                        found=False,
                    ).dict(),
                ),
            ],
        )
