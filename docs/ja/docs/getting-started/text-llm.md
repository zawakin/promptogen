`TextLLM` 抽象クラスは、テキストからテキストを生成する大規模言語モデル(LLM)のインターフェースです。

`TextLLM` は `generate` メソッドを持ちます。このメソッドは、テキストを受け取り、テキストを返します。

```python
class LLM(ABC):
    """Language model interface."""

    pass

class TextLLM(LLM, ABC):
    """Language model interface that generates text from text."""

    @abstractmethod
    def generate(self, input_text: str) -> str:
        pass
```

このようなインターフェースを定義することで、様々な大規模言語モデルを統一的に扱うことができます。

## OpenAI API を使用した例

このページでは、OpenAI API を使用した `TextLLM` の実装例を紹介します。
例えば、以下のような `generate_chat_completion` 関数を定義しておきます。

```python
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

def generate_chat_completion(text: str, model: str) -> str:
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        max_tokens=2048,
        stream=True,
    )
    raw_resp = ""
    for chunk in resp:
        chunk_content = chunk["choices"][0]["delta"].get("content", "")
        raw_resp += chunk_content

    return raw_resp
```

## 自作クラスを使った実装例

`TextLLM` クラスを継承することで、`TextLLM` を実装することができます。

```python
from promptogen.model.llm import TextLLM

class OpenAITextLLM(TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_chat_completion(text, self.model)
```

## FunctionBasedTextLLM

`FunctionBasedTextLLM` クラスは、テキストからテキストを生成する大規模言語モデル(LLM)の実装の一つです。

`(input_text: str) -> str` の関数を指定することで、`TextLLM` を実装することができます。

クラスを自作する場合に比べて、簡単に `TextLLM` を実装することができます。

```python
text_llm = FunctionBasedTextLLM(
    generate_text_by_text=lambda input_text: generate_chat_completion(input_text, "gpt-3.5-turbo"),
)
```

## 使い方

```python
text_llm = OpenAITextLLM("gpt-3.5-turbo")

print(text_llm.generate("Hello, I'm a human."))
# Hello! How can I assist you today as an AI?
```
