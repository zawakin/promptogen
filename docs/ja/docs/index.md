# PromptGen

# プロジェクトのビジョン
このプロジェクトでは、Pythonオブジェクトと大規模言語モデルのテキスト出力との間の変換に特化したライブラリを提供します。これはあなたが大規模言語モデルとの通信を気にせずに、テキスト出力の形式に集中できるようにするためのものです。

# 解決する問題
現在、大規模言語モデルを活用するライブラリの多くは、テキスト生成とパースの役割を担っていますが、同時に大規模言語モデルとの通信も行っています。これらの機能は一つのパッケージで提供されることが多く、ライブラリが大規模化し、一部の機能を改良または変更するのが難しくなっています。

# ソリューション
上記の問題を解決するため、大規模言語モデルとの通信とテキストの変換を分離することを提案します。PromptGen は、「ドメインモデルと文字列との変換」に特化します。つまり、このライブラリは以下の役割を果たします：

1. プロンプトの情報を表すデータクラスを定義する
1. プロンプトと入力データを任意のフォーマットの文字列に変換するフォーマッターを提供する
1. 大規模言語モデルからの出力を出力データに変換（パース）する

# ユーザーにとってのメリット
この分業の明確化により、ユーザーは自分が必要とする機能を選択し、それに最適化されたライブラリを使用することができます。また、新しい大規模言語モデルや通信ライブラリが開発されたときも、このライブラリはその影響を受けずに安定して機能します。ユーザーは大規模言語モデルに依存することなく、純粋に「どんな入力を与え、出力を得たいか」という点に集中して開発を行うことができます。

# 動作環境

Python 3.8 以上

# インストール
```console
$ pip install promptgen
```

# 使い方

## インポート

```python
import promptgen as pg
```

## 使い方

```python
# Define prompt as Python object
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
        input=pg.InputValue(text="This is a sample text to summarize."),
        output=pg.OutputValue(
            summary="This is a summary of the text.",
            keywords=["sample", "text", "summarize"],
        ),
    ),
    examples=[
        pg.Example(
            input=pg.InputValue(text="One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."),
            output=pg.OutputValue(
                summary="A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
                keywords=["friends", "park", "sports", "memories"],
            )
        )
    ],
)

# Define prompt formatter
formatter = pg.KeyValuePromptFormatter()

# Generate prompt to send to large language model
raw_req = formatter.format_prompt(summarizer, input_value)

# Send prompt to large language model and get response
# (implementation not shown)
raw_resp = generate_llm_response(raw_req)

# Parse response from large language model
summarized_resp = formatter.parse(raw_resp)
print(f'summary:\n{summarized_resp["summary"]}')
print('keywords:')
for keyword in summarized_resp["keywords"]:
    print(f'  - {keyword}')
```

出力:

```console
summary:
Software developers collaborate on projects using version control systems to create and maintain efficient code and solve implementation and user requirement issues.
keywords:
  - software engineering
  - developers
  - collaborate
  - version control systems
  - efficient code
  - implementation
  - user requirements
  - system optimization
```

## 大規模言語モデルとの通信

このライブラリは大規模言語モデルとの通信を行いません。そのため、大規模言語モデルとの通信には、[OpenAI Chat API](https://platform.openai.com/docs/api-reference/chat/create) などのライブラリを使用してください。

`generate_llm_response` 関数の実装例:

```python
import openai
openai.api_key = "<your-api-key>"

def generate_chat_stream_response(prompt: str, model: str):
        resp = openai.ChatCompletion.create(model=model, messages=[
            {'role': 'user', 'content': prompt}
        ], stream=True, max_tokens=2048)
        for chunk in resp:
            yield chunk['choices'][0]['delta'].get('content', '')


def generate_llm_response(prompt: str, model: str):
    s = ''
    for delta in generate_chat_stream_response(prompt, model):
        # print(delta, end='') # you can see the progress
        s += delta
    return s
```


# クイックスタートガイド

[クイックスタートガイド](quickstart.md)を参照してください。

# 依存関係

- [Pydantic](https://docs.pydantic.dev/latest/)

# 制限事項

- PromptGenのアップデートに伴い、json出力したプロンプトの互換性が失われる可能性があります。
- 動作検証に使用した大規模言語モデルは、OpenAI Chat API の `gpt-3.5-turbo`, `gpt-4` です。その他の大規模言語モデルでは動作検証を行っていません。特に、パーサーが正しく動作しないケースがある可能性があるため、ご注意ください。

# ライセンス

MITライセンス
