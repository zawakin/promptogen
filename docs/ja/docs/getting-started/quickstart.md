## PromptoGenとは

PromptoGenはPythonライブラリで、大規模言語モデルに対するプロンプトの生成と管理を支援します。このライブラリを使用すると、プロンプトとその入出力パラメータを定義し、それらをフォーマットして文字列に変換することができます。また、大規模言語モデルからの出力を解析し、Pythonオブジェクトに変換することも可能です。

PromptoGenは以下の機能を提供します:

- プロンプトとその入出力パラメータの定義
- プロンプトと入力パラメータのフォーマット（文字列化）
- 大規模言語モデルからの出力の解析とPythonオブジェクトへの変換

PromptoGenは、例えばOpenAIのGPT-3.5やGPT-4などの大規模言語モデルを利用する際の、プロンプトの生成と管理を効率化します。これにより、ユーザーはプロンプトの作成や管理に関する手間を軽減し、より多くの時間をモデルとの対話や、その結果の解析に費やすことができます。

![PromptoGenの概要](/ja/img/overview.png)

## インポート
    
```python
import promptogen as pg
```

## 簡単なプロンプトを作成する

まずは、簡単なプロンプトを作成してみましょう。このクイックスタートガイドでは、テキストを入力として受け取り、そのテキストの要約文とキーワードを出力するプロンプトを作成します。

つまり、 `(text: str) -> (summary: str, keywords: List[str])` という関数を実現するプロンプトを作成します。

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
| 入出力のテンプレート      | `template`                      | `pg.Example`                           |
| 入出力の例のリスト        | `examples`                      | `List[pg.Example]`                     |


これらの情報を使って、プロンプトを作成します。

```python
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
    template=pg.Example(
        input={'text': "This is a sample text to summarize."},
        output={
            'summary': "This is a summary of the text.",
            'keywords': ["sample", "text", "summarize"],
        },
    ),
    examples=[
        pg.Example(
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

## プロンプトを入力パラメータなしで文字列にフォーマットする

まずは、プロンプトを入力パラメータなしで文字列にフォーマットしてみましょう。

PromptoGenでは、プロンプトを文字列にするためのフォーマッターを柔軟に作成できます。

ここでは、入出力変数のキーとバリューを `key: value` の形式で出力する `KeyValuePromptFormatter` というフォーマッターを使用します。

入力パラメータなしで文字列にフォーマットするには、フォーマッターの `format_prompt_without_input` メソッドを使用します。
このメソッドは、プロンプトとフォーマッターを引数に取り、プロンプトを文字列にフォーマットします。

```python
formatter = pg.KeyValuePromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
```

コンソール出力:

```console
Summarize text and extract keywords.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text
  - keywords: Keywords extracted from text

Template:
Input:
text: "This is a sample text to summarize."
Output:
summary: """This is a summary of the text."""
keywords: ['sample', 'text', 'summarize']

Example 1:
Input:
text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
keywords: ['friends', 'park', 'sports', 'memories']
```

## プロンプトを入力パラメータありで文字列にフォーマットする

続いて、プロンプトを入力パラメータありで文字列にフォーマットしてみましょう。

入力パラメータは、 `dict` を使用して指定します。

プロンプトを入力パラメータ込みで文字列にフォーマットするには、`format_prompt` メソッドを使用します。

```python
input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.",
}
print(formatter.format_prompt(summarizer, input_value))
```

コンソール出力:

```console
Summarize text and extract keywords.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text
  - keywords: Keywords extracted from text

Template:
Input:
text: "This is a sample text to summarize."
Output:
summary: """This is a summary of the text."""
keywords: ['sample', 'text', 'summarize']

Example 1:
Input:
text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
keywords: ['friends', 'park', 'sports', 'memories']

--------

Input:
text: "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization."
Output:
```

## 大規模言語モデルを用いて出力を生成する

続いて、大規模言語モデルからの出力を生成してみましょう。

このライブラリでは、大規模言語モデルからの出力を生成するための機能は提供していませんが、OpenAI ChatGPT API などを用いることで実現できます。

ここでは、OpenAI ChatGPT API を用いて、入力テキストを要約したテキストを生成してみましょう。

```python
import openai
import os

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")


def generate_chat_stream_response(prompt: str, model: str):
        resp = openai.ChatCompletion.create(model=model, messages=[
            {'role': 'user', 'content': prompt}
        ], stream=True, max_tokens=2048)
        for chunk in resp:
            yield chunk['choices'][0]['delta'].get('content', '') # type: ignore


def generate_text_by_text(prompt: str, model: str):
    s = ''
    for delta in generate_chat_stream_response(prompt, model):
        s += delta
    return s
```



```python
raw_req = formatter.format_prompt(summarizer, input_value)
raw_resp = generate_text_by_text(raw_req, model='gpt-3.5-turbo')
print(raw_resp)
```

コンソール出力:


```console
summary: """Software developers collaborate using version control systems like Git to create and maintain efficient code and solve implementation and optimization issues."""
keywords: ['software engineering', 'developers', 'collaborate', 'projects', 'version control systems', 'Git', 'code', 'implementation complexities', 'evolving user requirements', 'system optimization']
```

## 出力をPythonオブジェクトに変換する

続いて、出力をPythonオブジェクトに変換してみましょう。
`formatter.parse` メソッドを使用することで、LLMからの出力文字列をプロンプトの出力パラメータを用いてパースできます。パースの結果はPythonの `dict` に格納されます。

```python
summarized_resp = formatter.parse(summarizer, raw_resp)
print(summarized_resp)
```

コンソール出力:

```console
{'summary': 'Software developers collaborate using version control systems like Git to create and maintain efficient code and solve implementation and optimization issues.', 'keywords': ['software engineering', 'developers', 'collaborate', 'projects', 'version control systems', 'Git', 'code', 'implementation complexities', 'evolving user requirements', 'system optimization']}
```

## まとめ

以上、PromptoGen の基本的な使い方を紹介しました。

ここまでの流れは、以下のようになります。

1. プロンプトを定義する
2. フォーマッターを定義する
3. フォーマッターを使って、プロンプトと入力パラメータを文字列にフォーマットする
4. 大規模言語モデルを用いて、出力を生成する
5. 出力をPythonオブジェクトに変換する

ここで紹介したのはシンプルな例ではありますが、PromptoGen を用いることで、より複雑なプロンプトや入出力パラメータを簡単に扱うことができます。

また、入力パタメータや出力パラメータとしてプロンプトそのものを指定することができるため、プロンプトを動的に生成することも可能です。
