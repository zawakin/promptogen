# PromptoGen

<a href="/" target="_blank"><img src="img/logo-bg-white.svg" style="width: 90%; padding-left: 10%;"></a>

----

:material-file-document-alert: ドキュメンテーション: https://promptogen.zawakin.dev/

:material-github: ソースコード: https://github.com/zawakin/promptogen

:material-rocket: クイックスタートガイドは[こちら](getting-started/installation.md)。

:material-earth: [English](/) | [日本語](/ja/)

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

- KeyValue形式フォーマット `key: value`
- JSON形式フォーマット `{"key": "value"}`
- etc.

### プロンプトフォーマット基本構造

プロンプト文字列は、以下のような基本的な構造を持ちます。

=== "Description"

    ```console title="Prompt Description" hl_lines="1"
    --8<-- "index/format_template_ja.txt:key_value_format_template"
    ```

=== "Input Parameters"

    ```console title="Input Parameters" hl_lines="3-6"
    --8<-- "index/format_template_ja.txt:key_value_format_template"
    ```

=== "Output Parameters"

    ```console title="Output Parameters" hl_lines="8-11"
    --8<-- "index/format_template_ja.txt:key_value_format_template"
    ```

=== "Template"

    ```console title="Template" hl_lines="13-21"
    --8<-- "index/format_template_ja.txt:key_value_format_template"
    ```

=== "Few-shot Examples"

    ```console title="Few-shot Examples" hl_lines="23-33"
    --8<-- "index/format_template_ja.txt:key_value_format_template"
    ```

=== "Input Value"

    ```console title="Input Value" hl_lines="37-40"
    --8<-- "index/format_template_ja.txt:key_value_format_template"
    ```


`key: value` 形式のプロンプトのフォーマットを使用するには、`pg.KeyValuePromptFormatter`を使用します。
パラメータ情報やテンプレートを表示するかどうかは `PromptFormatterConfig` で設定できます。

`formatter.format_prompt` メソッドを使用して、プロンプトとそれに対する入力を文字列に変換できます。

=== "KeyValue形式フォーマット"

    ```python hl_lines="8 13"
    import promptogen as pg

    summarizer = pg.Prompt(
        name="Text Summarizer and Keyword Extractor",
        # ...
    )

    formatter = pg.KeyValuePromptFormatter()

    input_value = {
        "text": "In the realm of software engineering, ...",
    }
    print(formatter.format_prompt(summarizer, input_value))
    ```

=== "JSON形式フォーマット"

    ```python hl_lines="8 13"
    import promptogen as pg

    summarizer = pg.Prompt(
        name="Text Summarizer and Keyword Extractor",
        # ...
    )

    formatter = pg.JsonPromptFormatter()

    input_value = {
        "text": "In the realm of software engineering, ...",
    }
    print(formatter.format_prompt(summarizer, input_value))
    ```

<!-- <> -->

=== "KeyValue形式フォーマット"

    ```console title="Console Output" hl_lines="12 14-15 19 21-22 27"
    --8<-- "index/format_template.txt:key_value_format_summarizer"
    ```

=== "JSON形式フォーマット"

    ````console title="Console Output" hl_lines="3-4 15-18 20-28 32-35 37-46 51-54"
    --8<-- "index/format_template.txt:json_format_summarizer"
    ````

### 大規模言語モデルからの出力のパース

さきほどのプロンプト文字列を入力として、大規模言語モデル(GPT-3.5, GPT-4など)から出力を得ます。

=== "KeyValue形式フォーマット"
    ```console title="LLM Output"
    summary: "This is a summary of the text."
    keywords: ['sample', 'text', 'summarize']
    ```

=== "JSON形式フォーマット"

    ````console title="LLM Output"
    ```json
    {
        "summary": "This is a summary of the text.",
        "keywords": ["sample", "text", "summarize"]
    }
    ```
    ````

`formatter.parse` を使って、出力をパースしてみます。

=== "KeyValue形式フォーマット"

    ```python hl_lines="3 7"
    import promptogen as pg

    formatter = pg.KeyValuePromptFormatter()

    raw_resp = """summary: "This is a summary of the text."
    keywords: ['sample', 'text', 'summarize']"""
    summarized_resp = formatter.parse(summarizer, raw_resp)
    print(summarized_resp)
    ```

    ```console title="Console Output"
    {'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
    ```


=== "JSON形式フォーマット"

    ```python hl_lines="3 11"
    import promptogen as pg

    formatter = pg.JsonPromptFormatter()

    raw_resp = """```json
    {
        "summary": "This is a summary of the text.",
        "keywords": ["sample", "text", "summarize"]
    }
    ```"""
    summarized_resp = formatter.parse(summarizer, raw_resp)
    print(summarized_resp)
    ```

    ```console title="Console Output"
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
