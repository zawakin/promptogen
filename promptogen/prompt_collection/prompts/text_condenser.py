from __future__ import annotations

from typing import List

from promptogen.model.prompt import IOExample, ParameterInfo, Prompt


class TextCondenserPrompt(Prompt):
    name: str = "TextCondenser"
    description: str = "Given a long sentence and some information, remove the parts that are irrelevant to the specified information. However, be careful not to drop more information than necessary. (Please output as is not only the parts that are clearly related, but also the parts that may be related."
    input_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="information", description="The information that needs to be preserved in the condensed text"
        ),
        ParameterInfo(name="text", description="The long text to be condensed"),
    ]
    output_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="result",
            description="a shorter version while ensuring the specified information and its relevant context are preserved",
        ),
    ]
    template: IOExample = IOExample(
        input={
            "information": "information",
            "text": "text",
        },
        output={
            "result": "result",
        },
    )
    examples: List[IOExample] = [
        IOExample(
            input={
                "information": "location of the city and its treasures",
                "text": "In the heart of the dense jungle lies the city of gold, untouched and unspoiled. It is believed that the city was abandoned centuries ago due to an unknown catastrophe. Legends say that the city still holds great treasures.",
            },
            output={
                "result": "The untapped city of gold, located in the dense jungle, is rumored to harbor great treasures.",
            },
        ),
        IOExample(
            input={
                "information": "major attraction of the exhibition",
                "text": "The exhibition showcased a wide range of art pieces from all over the world. The most notable piece was the Mona Lisa, attracting crowds from various countries to admire its beauty.",
            },
            output={
                "result": "The exhibition was notable for showcasing the globally admired art piece, the Mona Lisa.",
            },
        ),
        IOExample(
            input={
                "information": "launch and features of the new smartphone",
                "text": "The tech giant recently launched their newest smartphone model. Packed with the latest tech and impressive camera quality, it is set to compete directly with the leading competitors in the market.",
            },
            output={
                "result": "The tech giant just released a new smartphone, equipped with the latest technology and superior camera.",
            },
        ),
        IOExample(
            input={
                "information": "location of the city and its treasures",
                "text": "The tech giant recently launched their newest smartphone model. Packed with the latest tech and impressive camera quality, it is set to compete directly with the leading competitors in the market.",
            },
            output={
                "result": "",
            },
        ),
    ]
