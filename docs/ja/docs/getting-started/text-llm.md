## TextLLM: 大規模言語モデルの抽象化

PromptoGen では、 `pg.TextLLM`を介して、大規模言語モデル(LLM)とのテキスト生成を行います。このインターフェイスを理解し、適切に利用することは、このライブラリを最大限に活用するための鍵となります。

### 使用例:

```python
import promptogen as pg

class YourTextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_by_your_text_llm(text, self.model)

text_llm = YourTextLLM(model="your-model")
```

上記の例では、任意のLLMを使用するための`YourTextLLM`クラスを定義しています。実際のLLMへの接続やテキスト生成ロジックは、`generate_by_your_text_llm`メソッドに委譲されています。

### なぜ `pg.TextLLM` インターフェイスは重要か?

PromptoGenは、具体的なLLM (例: `gpt-3.5-turbo`, `gpt-4`) の実装から独立して設計されています。これにより、異なるLLMのバージョンや他の言語モデルを簡単に取り替えられるようになっています。この独立性を実現するために、`pg.TextLLM`インターフェイスが中心的な役割を果たしています。ユーザーはこのインターフェイスを通して、独自のLLM実装をPromptoGenに注入することができます。

このように、`pg.TextLLM`インターフェイスを通じて、PromptoGenは柔軟性と拡張性を保持しています。

## `TextLLM` について

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

Promptogenは、具体的なLLMに依存しないように設計されています。 `TextLLM` はその代表的な例です。
このようなインターフェースを定義することで、様々な大規模言語モデルを統一的に扱うことができます。

## 実装例1: 自作クラスを使った例

たとえば、 OpenAI API を使用した `TextLLM` の実装例を紹介します。
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

`TextLLM` クラスを継承することで、`TextLLM` を実装することができます。

```python
import promptogen as pg

class OpenAITextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_chat_completion(text, self.model)
```

## 実装例2: 関数を元にして `TextLLM` を実装する例

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

基本的に、 `pg.TextLLM` に依存するように実装を進めることで、 **LLMに依存しない汎用的なシステム** を構築しやすくなります。
