## `Prompt`

In PromptoGen, there is a data class (`pg.Prompt`) prepared to represent prompts.
Using this data class, you can create prompts.
This data class inherits from `pydantic.BaseModel`.

To create a prompt, the following information is required.

| Item                   | Argument Name                  | Type                                  |
|-----------------------|--------------------------------|---------------------------------------|
| Prompt name            | `name`                         | `str`                                 |
| Prompt description     | `description`                  | `str`                                 |
| List of input parameters | `input_parameters`           | `List[pg.ParameterInfo]`              |
| List of output parameters | `output_parameters`          | `List[pg.ParameterInfo]`              |
| Input-output template    | `template`                   | `pg.IOExample`                        |
| List of input-output examples | `examples`              | `List[pg.IOExample]`                  |


```python
class Prompt(DataClass):
    """A prompt.

    Attributes:
        name: The name of the prompt.
        description: A description of the prompt.
        input_parameters: The parameter information for the prompt's input.
        output_parameters: The parameter information for the prompt's output.
        template: An example of the prompt.
        examples: A list of examples for the prompt.
    """

    name: str
    description: str
    input_parameters: List[ParameterInfo]
    output_parameters: List[ParameterInfo]
    template: IOExample
    examples: List[IOExample]
```


## `ParameterInfo`

`ParameterInfo` is a data class designed to represent the information of input and output parameters of the prompt. It holds the name and description of the parameter.

```python
class ParameterInfo(DataClass):
    """Information about a parameter.

    Attributes:
        description: A description of the parameter.
    """

    name: str
    description: str
```


## `IOExample`

`IOExample` is a data class designed to represent examples of a prompt's input and output.

```python
Value: TypeAlias = Dict[str, Any]

class IOExample(DataClass):
    """A few-shot example of a prompt.

    Attributes:
        input: The input for the prompt.
        output: The output from the prompt.
    """

    input: Value # dict[str, Any]
    output: Value # dict[str, Any]
```

Using the above information, you can create a prompt.

```python
import promptogen as pg

summarizer = pg.Prompt(
    name="Text Summarizer and Keyword Extractor",
    description="Summarize text and extract keywords.",
    input_parameters=[
        pg.ParameterInfo(name="text", description="Text to summarize"),
    ],
    output_parameters=[
        pg.ParameterInfo(name="summary", description="Summary of text"),
        pg.ParameterInfo(name="keywords", description="Keywords extracted from text"),
    ],
    template=pg.IOExample(
        input={'text': "This is a sample text to summarize."},
        output={
            'summary': "This is a summary of the text.",
            'keywords': ["sample", "text", "summarize"],
        },
    ),
    examples=[
        pg.IOExample(
            input={
                'text': "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."},
            output={
                'summary': "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
                'keywords': ["friends", "park", "sports", "memories"],
            },
        )
    ],
)
```

## Displaying the Prompt

You can display the information of the created prompt using the `print` function.

```python
print(summarizer)
```

```text
Text Summarizer and Keyword Extractor: (text: str) -> (summary: str, keywords: list)

Description
-----------
Summarize text and extract keywords.

Input Parameters
----------------
- text (str): Text to summarize

Output Parameters
-----------------
- summary (str): Summary of text
- keywords (list): Keywords extracted from text
```

## Saving the Prompt

You can save the created prompt using the `Prompt.to_json_file` method.

```python
summarizer.to_json_file("summarizer.json")
```

## Loading the Prompt

You can load a saved prompt using the `Prompt.from_json_file` method.

```python
summarizer = pg.Prompt.from_json_file("summarizer.json")
```

## Representing the Prompt in JSON Format

Since `Prompt` inherits from pydantic's `BaseModel`, you can represent it in JSON format using the `Prompt.model_dump_json` method.

```python
print(summarizer.model_dump_json(indent=4))
```

```json
{
    "name": "Text Summarizer and Keyword Extractor",
    "description": "Summarize text and extract keywords.",
    "input_parameters": [
        {
            "name": "text",
            "description": "Text to summarize"
        }
    ],
    "output_parameters": [
        {
            "name": "summary",
            "description": "Summary of text"
        },
        {
            "name": "keywords",
            "description": "Keywords extracted from text"
        }
    ],
    "template": {
        "input": {
            "text": "This is a sample text to summarize."
        },
        "output": {
            "summary": "This is a summary of the text.",
            'keywords': [
                "sample",
                "text",
                "summarize"
            ]
        }
    },
    "examples": [
        {
            "input": {
                "text": "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
            },
            "output": {
                "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
                'keywords': [
                    "friends",
                    "park",
                    "sports",
                    "memories"
                ]
            }
        }
    ]
}
```
