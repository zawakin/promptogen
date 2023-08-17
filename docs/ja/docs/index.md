# PromptoGen

<a href="/" target="_blank"><img src="img/logo-light-mode.svg#only-light" style="width: 90%; padding-left: 10%;"></a>
<a href="/" target="_blank"><img src="img/logo-dark-mode.svg#only-dark" style="width: 90%; padding-left: 10%;"></a>

<p style="text-align: center;">
    <em>LLMとPythonをシームレスにつなぐ。</em>
</p>

----

:material-file-document-alert: ドキュメンテーション: https://promptogen.zawakin.dev

:material-github: ソースコード: https://github.com/zawakin/promptogen

:material-rocket: クイックスタートガイドは[こちら](getting-started/installation.md)。

:material-earth: [English](/) | [日本語](/ja/)

----

## :material-book-multiple: PromptoGenについて
### :material-lightbulb: PromptoGenのプロジェクトビジョン

**「効率的で拡張可能な、大規模言語モデル(LLM)とのコミュニケーションを実現する」**

1. **LLM入出力とPythonオブジェクトのシームレスな変換**：LLMとのコミュニケーションを自然に、かつ効率的に行います。
2. **独自の抽象化インターフェイス**：ユーザーに高いカスタマイズ性と拡張性を提供します。
3. **LLM通信への依存性排除**：将来のLLMの進化や変更にも柔軟に対応できる堅牢なシステムを構築できるようにすることを目指します。

### :material-thought-bubble: 解決すべき課題

他のライブラリ: LLM通信からテキスト生成・パースまで担当していることが多いため、以下の課題があります。

1. :material-thought-bubble: **プロンプトエンジニアリングのエコシステムが形成されにくい**
2. :material-thought-bubble: **LLMに強く依存しているため、LLMの変更・進化に弱い**
3. :material-thought-bubble: **実装が複雑で、カスタマイズ性が低い**

### :material-check-circle: ソリューション

1. :material-check-circle: **`Prompt`データクラス**: **プロンプトエンジニアリングのエコシステム形成**
    - LLMコミュニケーションの基本情報定義（名前、説明、入出力情報、テンプレート、使用例）
2. :material-check-circle: **`TextLLM`インターフェイス**: **LLM実装からの独立性確保**
    - データクラスライブラリ`Pydantic`だけへの依存で、LLMの進化にロバスト
    - LLMとの通信は`TextLLM`インターフェイスを介す
3. :material-check-circle: **`PromptFormatter`インターフェイス**: **カスタマイズ性の向上**
    - 任意のフォーマッターを定義できる
    - `Prompt`と入力からプロンプト文字列生成
    - LLMテキスト出力をPythonデータ構造に変換

### :material-star-shooting: ユーザーにとってのメリット
- :material-puzzle: **モジュール性**: 組み合わせ自由
- :material-plus: **拡張性**: 独自フォーマッターやパーサー追加可
- :material-shield-half-full: **独立性**: 新しいモデルやライブラリの影響なし
- :material-wrench: **メンテナンス性**: 管理やトラブルシューティングが簡単
- :material-clock: **開発効率**: LLMごとに実装を変更する必要なし

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
import promptogen as pg

summarizer = pg.Prompt.from_json_file("summarizer.json")
```

### TextLLM: 柔軟なLLM連携

`pg.TextLLM`を介すことで、PromptoGenは多種多様な大規模言語モデル(LLM)との連携を実現します。

```python title="TextLLMインターフェイスの実装例"
import promptogen as pg

class YourTextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_by_your_text_llm(text, self.model)

text_llm = YourTextLLM(model="your-model")
```

このインターフェイスの採用により、PromptoGenは異なるLLMやそのバージョンをスムーズに組み込むことが可能になります。ユーザーはLLMによらない一貫した方法で、様々なLLMを活用できるようになります。

### PromptRunner: プロンプト実行、効率的に

`pg.PromptRunner`は、プロンプトの実行をシンプルに、かつ効率的にサポートします。

```python hl_lines="7 18" title="PromptRunnerを使ったプロンプト実行"
import promptogen as pg

# `pg.TextLLM`インターフェイスを実装したLLMを用意
text_llm = YourTextLLM(model="your-model")

formatter = pg.KeyValuePromptFormatter()
runner = pg.TextLLMPromptRunner(llm=text_llm, formatter=formatter)

summarizer = pg.Prompt(
    name="Text Summarizer and Keyword Extractor",
    # ...
)

input_value = {
    "text": "In the realm of software engineering, ...",
}

output_value = runner.run_prompt(summarizer, input_value)
print(output_value)
```

このツールの利点:

1. **抽象化**: ユーザーは具体的なLLMの実装を意識せずにプロンプトを実行できます。
2. **一貫性**: 同じプロンプトを異なるLLMで実行する際の変更を最小限に抑えられます。
3. **拡張性**: 新しいプロンプトの追加や既存プロンプトの修正が簡単です。

`pg.PromptRunner`は、PromptoGenを使ったプロンプトの実行をより直感的で効率的にするためのキーとなるツールです。

## クイックスタートガイド

[クイックスタートガイド](getting-started/quickstart.md)を参照してください。

## 応用例

[応用例](examples/index.md)を参照してください。

- プロンプトの自動生成
- LLM入出力推論の生成

## 依存ライブラリ

- [Pydantic >= 2.0.3](https://docs.pydantic.dev/latest/) ... データクラスの定義に使用

## 制限事項

- PromptoGenのアップデートに伴い、json出力したプロンプトの互換性が失われる可能性があります。
- 動作検証に使用した大規模言語モデルは、OpenAI Chat API の `gpt-3.5-turbo`, `gpt-3.5-tubrbo-16k`, `gpt-4` や Meta の `Llama 2` です。その他の大規模言語モデルでは動作検証を行っていません。特に、パーサーが正しく動作しないケースがある可能性があるため、ご注意ください。

## コントリビューション

バグの報告、新機能の提案、プルリクエスト等は大歓迎です！詳しくは[コントリビューション](contributing.md)をご覧ください。

## ライセンス

MITライセンス
