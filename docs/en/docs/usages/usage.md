# 使い方

最も基本的な使い方は以下の通りです。

1. 使用するLLMを定義する
1. プロンプトの要件を定義する
1. PromptCreator でプロンプトを自動生成する
1. PromptRunner でプロンプトを実行する

## インポート
    
```python
import promptogen as pg
```

## LLMの定義

Large Language Model(LLM) とは、テキストを生成するための大規模な言語モデルのことです。PromptoGen では、LLMを定義するためのクラスを提供しています。


`pg.TextLLM` は抽象クラスであり、`generate` メソッドを実装する必要があります。


```python
class YourTextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        # Generate text using your LLM
        return generated_text
```

```python
llm = YourTextLLM(model='your-model')
```

このように抽象クラスを継承したクラスを定義することで、独自のLLMを定義することができます。

より簡単にLLMを定義するために、 `(text: str) -> (generated_text: str)` のような関数を渡すこともできます。
`FunctionBasedTextLLM` クラスは、このような関数をラップしたLLMを定義するためのクラスです。

```python
def generator_func(text: str) -> str:
    # Generate text using your LLM
    return generated_text

llm = pg.FunctionBasedTextLLM(generator_func)
```

## PromptFormatter の定義

PromptFormatter は、プロンプトを文字列にフォーマットするためのクラスです。PromptoGen では、様々な形式のフォーマッターをサポートしています。

```python
formatter = pg.KeyValuePromptFormatter()
```

## PromptRunner の定義

PromptRunner は、プロンプトを実行するためのクラスです。

`run_prompt` メソッドは、以下のように定義されています。

```python
def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
    """Run the given prompt and return the result.

    Args:
        prompt: The prompt to run. It must be an instance of Prompt.
        input_value: The input value to use. It must be an instance of Value, which is a dict.
    """
    raw_req = self.formatter.format_prompt(prompt, input_value)
    raw_resp = self.text_llm.generate(raw_req)
    resp = self.formatter.parse(prompt, raw_resp)
    return resp
```

つまり、`run_prompt` メソッドは、プロンプトと入力パラメータを受け取り、LLMを用いてプロンプトを実行し、出力を返すメソッドです。

```python
prompt_runner = pg.PromptRunner(llm, formatter)
```


## プロンプトを作成する

ここでは、 `PromptCreatorPrompt` を用いてプロンプトを自動生成する方法を紹介します。

```python
from promptogen.prompt_collection import PromptCreatorPrompt

prompt_creator_prompt = PromptCreatorPrompt()

print(prompt_creator_prompt)
```

```console
PromptCreator: (description: str, background: str) -> (prompt: Prompt)

Description
-----------
Create a prompt from the given description and background. Use the given description as the prompt description as is. Consider background information to make the prompt more specific.

Input Parameters
----------------
- description (str): description of the prompt; this will be used as the prompt description as is
- background (str): background of the prompt

Output Parameters
-----------------
- prompt (Prompt): A prompt which has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.

Examples Count
--------------
2
```

`PromptCreatorPrompt` は、プロンプトを生成するためのプロンプトです。このプロンプトの入力パラメータとして、プロンプトの説明と背景情報を渡すことで、プロンプトを自動生成することができます。

実際にプロンプトを生成してみましょう。

```python
input_value = {
    "description": "Answer the question for the given context.",
    "background": "(context: str, question: str) -> (answer: str)",
}
resp = prompt_runner.run_prompt(prompt_creator_prompt, input_value=input_value)
```

`resp` は `dict` 型のオブジェクトなので、 `Prompt` クラスのインスタンスに変換してみましょう。

```python
context_qa_prompt = pg.Prompt.from_dict(resp["prompt"])
```

このように自動生成したプロンプトの中身を確認し、場合によっては修正することで、より良いプロンプトを作成することができます。
一度 json 形式に変換し、テキストエディタで編集することも可能です。

```python
context_qa_prompt.to_json_file("context_qa_prompt.json")
```

編集したプロンプトを読み込みます。

```python
context_qa_prompt = pg.Prompt.from_json_file("context_qa_prompt.json")
```

## プロンプトを実行する

プロンプトを実行してみましょう。

```python
input_value = {
    "context": "The quick brown fox jumps over the lazy dog.",
    "question": "What does the fox jump over?",
}

output_value = prompt_runner.run_prompt(context_qa_prompt, input_value=input_value)

print(output_value["answer"])
```

```console
the lazy dog
```

## 追加機能：回答の理由を生成する

```python
from promptogen.prompt_tool import TextLLMReasoningExtractor

reasoning_extractor = TextLLMReasoningExtractor(
    text_llm=llm,
    reasoning_template="This is because ... So the answer is ...",
)

print(
    reasoning_extractor.generate_reasoning(
        prompt=context_qa_prompt,
        example=pg.IOExample(
            input=input_value,
            output=output_value,
        ),
    ).reasoning
)
# -> This is because the input text "context" provides the information that the quick brown fox jumps over the lazy dog. The input question "question" asks what the fox jumps over. Therefore, the answer is "The fox jumps over the lazy dog" which is derived directly from the context information.
```
