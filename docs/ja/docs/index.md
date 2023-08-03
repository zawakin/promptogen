# PromptGen

----

ドキュメンテーション: https://promptgen.zawakin.dev/ja/

ソースコード: https://github.com/zawakin/promptgen

クイックスタートガイドは[こちら](quickstart.md)

----


## PromptGenについて

### プロジェクトのビジョン

PromptGenはPythonオブジェクトと大規模言語モデルのテキスト出力間の変換に専念します。これにより、大規模言語モデルとの直接的な通信を気にすることなく、ユーザーはプロンプトの生成と解析に集中できます。

### 解決する問題
大規模言語モデルの利用に際して、多くのライブラリがモデルとの通信からテキストの生成、パースまで幅広い機能を包括しています。その結果、必要な機能を取り出したり、一部の機能をカスタマイズしたりするのが困難になっています。

### ソリューション

この問題を解決するために、PromptGenは"ドメインモデルと文字列との変換"という具体的な部分に焦点を当てています。つまり、大規模言語モデルとの直接的な通信を考慮せずに、次のような特定の役割に集中できます：

1. 大規模言語モデルへのコマンドを表現するためのデータクラスを定義します。
1. プロンプトや入力データを任意のフォーマットの文字列に変換するフォーマッターを提供します。
1. 大規模言語モデルからのテキスト出力を適切な出力データに変換（パース）します。

このアプローチにより、PromptGenは独立して機能し、新しい大規模言語モデルや通信ライブラリが登場した際にも影響を受けることなく、その機能を続けることが可能です。

### ユーザーにとってのメリット

1. **モジュール性**: PromptGenは特定の部分（文字列とドメインモデルの変換）に特化しているため、他の大規模言語モデルや通信ライブラリと自由に組み合わせて使用できます。このようなモジュール性は、ユーザーが自分のニーズに最適なソリューションを構築する柔軟性を提供します。

1. **拡張性**: PromptGenはユーザーが自分のフォーマッターとパーサーを定義し、追加することが可能です。これにより、特定のプロジェクトやユースケースに最適化された変換ロジックを実装することが可能になります。

1. **独立性**: PromptGenは大規模言語モデルや通信ライブラリに依存せず、これらがどのように進化してもその機能は影響を受けません。これにより、新しいモデルやライブラリが登場した際にも、既存のコードを大幅に書き換える必要がなく、安心して使用を続けることが可能です。

1. **メンテナンス性**: PromptGenのソースコードは、特定の部分に焦点を絞った設計により、他の全機能を含むライブラリよりも管理が容易です。このため、問題が発生した場合のトラブルシューティングが簡単になり、また新しい機能の追加も容易になります。

1. **開発効率**: PromptGenを使用することで、開発者は大規模言語モデルとの通信や他の複雑な処理について心配することなく、プロンプトの生成と解析に集中できます。これにより、より高品質なアプリケーションをより短時間で開発することが可能になります。


## 動作環境

Python 3.8 以上

## インストール
```console
$ pip install promptgen
```

## 使用例

### プロンプトの作成

```python
import promptgen as pg

summarizer = pg.Prompt(
    name="Text Summarizer",
    description="Summarize text.",
    input_parameters=[
        pg.ParameterInfo(name="text", description="Text to summarize"),
    ],
    output_parameters=[
        pg.ParameterInfo(name="summary", description="Summary of text"),
    ],
    template=pg.Example(
        input={
            "text": "This is a sample text to summarize.",
        },
        output={
            "summary": "This is a summary of the text.",
        }
    ),
    examples=[
        # few-shots examples
    ],
)

print(summarizer)
```

コンソール出力:

```console
Text Summarizer: (text: str) -> (summary: str)

Description
-----------
Summarize text.

Input Parameters
----------------
- text (str): Text to summarize

Output Parameters
-----------------
- summary (str): Summary of text

Examples Count
--------------
0
```

### プロンプトのフォーマット

PromptGenでは様々な形式のフォーマットをサポートしています。

- `key: value`形式
- JSON形式
- 単一テキスト形式
- etc.

ここでは、`key: value`形式のフォーマットを使用します。

```python
formatter = pg.KeyValuePromptFormatter()

input_value = {
    "text": "In the realm of software engineering, ...",
}
print(formatter.format_prompt(summarizer, input_value))
```

コンソール出力:

```console
Summarize text.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text

Template:
Input:
text: 'This is a sample text to summarize.'
Output:
summary: 'This is a summary of the text.'

--------

Input:
text: 'In the realm of software engineering, ...'
Output:
```

### 大規模言語モデルからの出力のパース

さきほどのプロンプト文字列を入力として、大規模言語モデル(GPT-3.5, GPT-4など)から出力を得ます。

```console
summary: 'Software developers collaborate on projects ...'
```

この出力をパースします。

```python
summarized_resp = formatter.parse(raw_resp)
print('summary:')
print(f'{summarized_resp["summary"]}')
```

コンソール出力:

```console
Software developers collaborate on projects ...
```

### プロンプトの保存

```python
summarizer.to_json_file("summarizer.json")
```

### プロンプトの読み込み

```python
summarizer = pg.Prompt.from_json_file("summarizer.json")
```


### クイックスタートガイド

[クイックスタートガイド](quickstart.md)を参照してください。

## 依存ライブラリ

- [Pydantic](https://docs.pydantic.dev/latest/) ... データクラスの定義に使用

## 制限事項

- PromptGenのアップデートに伴い、json出力したプロンプトの互換性が失われる可能性があります。
- 動作検証に使用した大規模言語モデルは、OpenAI Chat API の `gpt-3.5-turbo`, `gpt-4` や Meta の `Llama 2` です。その他の大規模言語モデルでは動作検証を行っていません。特に、パーサーが正しく動作しないケースがある可能性があるため、ご注意ください。

## コントリビューション

バグの報告、新機能の提案、プルリクエスト等は大歓迎です！詳しくは[コントリビューション](contributing.md)をご覧ください。

## ライセンス

MITライセンス
