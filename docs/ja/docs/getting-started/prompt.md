## `Prompt`

PromptoGenには、プロンプトを表現するためのデータクラス(`pg.Prompt`)が用意されています。
このデータクラスを使って、プロンプトを作成します。
このデータクラスは `pydantic.BaseModel` を継承しています。

プロンプトを作成するには、以下の情報が必要です。


| 項目                  | 引数名                           | 型                                      |
|-----------------------|--------------------------------|---------------------------------------|
| プロンプトの名前          | `name`                          | `str`                                  |
| プロンプトの説明          | `description`                  | `str`                                  |
| 入力パラメータのリスト      | `input_parameters`              | `List[pg.ParameterInfo]`               |
| 出力パラメータのリスト      | `output_parameters`             | `List[pg.ParameterInfo]`               |
| 入出力のテンプレート      | `template`                      | `pg.IOExample`                           |
| 入出力の例のリスト        | `examples`                      | `List[pg.IOExample]`                     |


```python
class Prompt(DataClass):
    """A prompt.

    Attributes:
        name: The name of the prompt.
        description: A description of the prompt.
        input_parameters: The parameter information of the prompt's input.
        output_parameters: The parameter information of the prompt's output.
        template: An example of the prompt.
        examples: A list of examples of the prompt.
    """

    name: str
    description: str
    input_parameters: List[ParameterInfo]
    output_parameters: List[ParameterInfo]
    template: IOExample
    examples: List[IOExample]
```


## `ParameterInfo`

`ParameterInfo` は、プロンプトの入力パラメータと出力パラメータの情報を表現するためのデータクラスです。
パラメータの名前と説明を持ちます。

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

`IOExample` は、プロンプトの入出力の例を表現するためのデータクラスです。

```python
Value: TypeAlias = Dict[str, Any]

class IOExample(DataClass):
    """An few-shot example of a prompt.

    Attributes:
        input: The input to the prompt.
        output: The output of the prompt.
    """

    input: Value # dict[str, Any]
    output: Value # dict[str, Any]
```


これらの情報を使って、プロンプトを作成します。

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

## プロンプトの表示

作成したプロンプトの情報は、`print` 関数で表示することができます。

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

## プロンプトの保存

作成したプロンプトは、`Prompt.to_json_file` メソッドで保存することができます。

```python
summarizer.to_json_file("summarizer.json")
```

## プロンプトの読み込み

保存したプロンプトは、`Prompt.from_json_file` メソッドで読み込むことができます。

```python
summarizer = pg.Prompt.from_json_file("summarizer.json")
```

## JSON形式でのプロンプトの表現

`Prompt` は pydantic の `BaseModel` を継承しているため、`Prompt.model_dump_json` メソッドで JSON 形式で表現することができます。

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
            "keywords": [
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
                "keywords": [
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
