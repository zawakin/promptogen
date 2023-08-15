# PromptoGen

<a href="/" target="_blank"><img src="img/logo-bg-white.svg" style="width: 90%; padding-left: 10%;"></a>

----

:material-file-document-alert: ドキュメンテーション: https://promptogen.zawakin.dev/

:material-source-repository: ソースコード: https://github.com/zawakin/promptogen

:material-rocket: クイックスタートガイドは[こちら](getting-started/installation.md)。

----

## :material-book-multiple: PromptoGenについて

### :material-lightbulb: プロジェクトのビジョン

PromptoGenは、大規模言語モデルのテキスト出力とPythonオブジェクト間の変換を助けます。直接的な大規模言語モデルとの通信を気にせず、プロンプト生成と解析に専念できます。

### :material-thought-bubble: 解決する問題

多くのライブラリは、大規模言語モデルとの通信からテキスト生成・パースまでを全て担当します。これにより、特定の機能のカスタマイズが難しくなります。

### :material-check-circle: ソリューション

PromptoGenは、LLM（Large Language Model）とのコミュニケーションを円滑化するための言語変換ツールとして機能します。以下の手順で動作するのがその特徴です。

1. **`Prompt`データクラスの利用**:

    - このデータクラスは、LLMとのコミュニケーションにおけるプロンプトの基本情報やその形式を定義するためのものです。
    - 各`Prompt`には、プロンプトの名前、説明、入力・出力のパラメータ情報、そして具体的な使用例が含まれています。

2. **`PromptFormatter`によるプロンプト文字列の生成と出力のパース**:

    - `PromptFormatter`は`Prompt`と入力値を受け取り、これをLLMに送信できる形のプロンプト文字列に変換します。
    - また、LLMからのテキスト形式の出力を、対応する`Prompt`の情報を基にして、プログラムが扱いやすいPythonのデータ構造（特にdict）に変換します。

### :material-star-shooting: ユーザーにとってのメリット

1. **モジュール性**: 他のモデルやライブラリと組み合わせ自由
1. **拡張性**: 独自のフォーマッターやパーサーを追加可能
1. **独立性**: 新しい言語モデルやライブラリの影響を受けません
1. **メンテナンス性**: 管理・トラブルシューティングが簡単
1. **開発効率**: 大規模言語モデルとの通信の心配なしで開発に専念

## :material-laptop: 動作環境

Python 3.8 以上

## インストール
```sh
pip install promptogen
```

## インポート
```python
import promptogen as pg
```

## 使い方

### プロンプトの作成

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

### プロンプトのフォーマット

`Prompt` クラスのインスタンスを実際にLLMに送信するために、文字列に変換する必要があります。PromptoGenでは、`pg.PromptFormatter`を使用して、プロンプトを任意の形式の文字列に変換することができます。

PromptoGenでは様々な形式のフォーマットをサポートしています。

- `key: value`形式
- JSON形式
- etc.

### KeyValue形式フォーマット基本構造

KeyValue形式のプロンプトフォーマットは、以下のような基本的な構造を持ちます。
パラメータ情報やテンプレートを表示するかどうかは `PromptFormatterConfig` で設定できます。

```
<プロンプト説明>

Input Parameters:
  - <入力パラメーター1の説明>
  - <入力パラメーター2の説明>
  - ...

Output Parameters:
    - <出力パラメーター1の説明>
    - <出力パラメーター2の説明>
    - ...

Template:
Input:
<入力パラメーター1の名前>: <入力パラメーター1の例>
<入力パラメーター2の名前>: <入力パラメーター2の例>
...
Output:
<出力パラメーター1の名前>: <出力パラメーター1の例>
<出力パラメーター2の名前>: <出力パラメーター2の例>
...

Example 1:
Input:
<入力パラメーター1の名前>: <入力パラメーター1の値>
<入力パラメーター2の名前>: <入力パラメーター2の値>
...
Output:
<出力パラメーター1の名前>: <出力パラメーター1の値>
<出力パラメーター2の名前>: <出力パラメーター2の値>
...

...
```


`key: value` 形式のプロンプトのフォーマットを使用するには、`pg.KeyValuePromptFormatter`を使用します。

`formatter.format_prompt` メソッドを使用して、プロンプトとそれに対する入力を文字列に変換できます。

```python
formatter = pg.KeyValuePromptFormatter()

input_value = {
    "text": "In the realm of software engineering, ...",
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
text: "In the realm of software engineering, ..."
Output:
```


### JSON形式のプロンプトのフォーマット

`pg.JsonPromptFormatter`を使用すると、プロンプトとその入力をJSON形式の文字列に変換できます。

```python
formatter = pg.JsonPromptFormatter()

input_value = {
    "text": "In the realm of software engineering, ...",
}
print(formatter.format_prompt(summarizer, input_value))
```

````console
Summarize text and extract keywords.

Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text
  - keywords: Keywords extracted from text

Template:
Input:
```json
{
 "text": "This is a sample text to summarize."
}```
Output:
```json
{
 "summary": "This is a summary of the text.",
 "keywords": [
  "sample",
  "text",
  "summarize"
 ]
}```

Example 1:
Input:
```json
{
 "text": "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
}```
Output:
```json
{
 "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
 "keywords": [
  "friends",
  "park",
  "sports",
  "memories"
 ]
}```

--------

Input:
```json
{
 "text": "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization."
}```
Output:
````

### 大規模言語モデルからの出力のパース

さきほどのプロンプト文字列を入力として、大規模言語モデル(GPT-3.5, GPT-4など)から出力を得ます。

```console
summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']
```

この出力をパースします。

```python
formatter = pg.KeyValuePromptFormatter()

raw_resp = """summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']"""
summarized_resp = formatter.parse(summarizer, raw_resp)
print(summarized_resp)
```

コンソール出力:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```

### プロンプトの保存

```python
summarizer.to_json_file("summarizer.json")
```

### プロンプトの読み込み

```python
summarizer = pg.Prompt.from_json_file("summarizer.json")
```


## クイックスタートガイド

[クイックスタートガイド](getting-started/quickstart.md)を参照してください。

## 応用例

[応用例](examples/index.md)を参照してください。

## 依存ライブラリ

- [Pydantic](https://docs.pydantic.dev/latest/) ... データクラスの定義に使用

## 制限事項

- PromptoGenのアップデートに伴い、json出力したプロンプトの互換性が失われる可能性があります。
- 動作検証に使用した大規模言語モデルは、OpenAI Chat API の `gpt-3.5-turbo`, `gpt-4` や Meta の `Llama 2` です。その他の大規模言語モデルでは動作検証を行っていません。特に、パーサーが正しく動作しないケースがある可能性があるため、ご注意ください。

## コントリビューション

バグの報告、新機能の提案、プルリクエスト等は大歓迎です！詳しくは[コントリビューション](contributing.md)をご覧ください。

## ライセンス

MITライセンス
