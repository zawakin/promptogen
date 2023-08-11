from __future__ import annotations

from typing import List

from promptogen.model.dataclass import DataClass
from promptogen.model.prompt import IOExample, ParameterInfo, Prompt


class TextSummarizerPrompt(Prompt):
    name: str = "Summarization"
    description: str = "Summarize the text into a shorter text."
    input_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="text",
            description="text to summarize",
        ),
    ]
    output_parameters: List[ParameterInfo] = [
        ParameterInfo(
            name="summary",
            description="summary of the text",
        ),
    ]
    template: IOExample = IOExample(
        input={
            "text": "text",
        },
        output={
            "summary": "summary",
        },
    )
    examples: List[IOExample] = [
        IOExample(
            input={
                "text": """Once upon a time, in a world filled with wonder and whimsy, there existed a small, peculiar village named Eldorina. This village was unlike any other, for it was inhabited by a variety of magical creatures, each with their own unique talents and quirks.

At the heart of Eldorina stood a grand library, where knowledge from across the realms was stored and studied. The library was managed by an ancient dragon named Biblios, who had the power to summon any book he desired, from the most mundane to the most enchanted.

The residents of Eldorina lived in harmony, their talents complementing each other and contributing to the overall magic of the village. There was Floriana, the fairy botanist, who could make flowers bloom with a mere touch; Gilby, the gnome inventor, whose creations could perform the most extraordinary tasks; and many more.

One day, a mysterious wanderer arrived in Eldorina. His name was Vesper, and he was a collector of stories. Vesper's arrival was heralded by a sudden eclipse, casting an eerie darkness over the village. The villagers were curious and cautious, unsure of what to make of the stranger in their midst."""
            },
            output={
                "summary": "In the magical village of Eldorina, inhabited by various magical creatures, a grand library managed by an ancient dragon named Biblios stands at the heart of the village. The residents live in harmony, each contributing their unique talents. One day, a mysterious wanderer named Vesper, a collector of stories, arrives in the village, causing an eclipse and leaving the villagers curious and cautious.",
            },
        ),
        IOExample(
            input={
                "text": """**Astonishing Discovery: Underground City Found Beneath Local Park**

*by Alexia Pennington*

In an unexpected turn of events, a previously undiscovered underground city has been found beneath the popular Greenfield Park in the quiet town of Willowsville. Local residents are astonished and thrilled by the discovery, which has attracted the attention of archaeologists and historians from around the globe.

The hidden city was uncovered last Sunday when park maintenance worker, Jim Pritchard, accidentally stumbled upon a concealed entrance while attempting to repair an irrigation issue. Pritchard was astounded to find an intricately designed tunnel that led to the entrance of the underground city.

\"I couldn't believe my eyes," said Pritchard. "One moment I was digging to fix a pipe, and the next, I was looking at the entrance to a whole new world.\""""
            },
            output={
                "summary": "An undiscovered underground city has been found beneath Greenfield Park in Willowsville. The hidden city was uncovered accidentally by a park maintenance worker, Jim Pritchard, while repairing an irrigation issue. The discovery has attracted the attention of archaeologists and historians worldwide.",
            },
        ),
    ]
