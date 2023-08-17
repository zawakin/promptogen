## TextLLM: Abstraction of Large Language Models

With PromptoGen, text generation with Large Language Models (LLM) is done via `pg.TextLLM`. Understanding and using this interface properly is key to making the most of this library.

### Usage Example:

```python
import promptogen as pg

class YourTextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_by_your_text_llm(text, self.model)

text_llm = YourTextLLM(model="your-model")
```

In the example above, the `YourTextLLM` class is defined to use any desired LLM. The actual connection to the LLM and text generation logic is delegated to the `generate_by_your_text_llm` method.

### Why is the `pg.TextLLM` interface important?

PromptoGen is designed to be independent from specific LLM implementations (e.g., `gpt-3.5-turbo`, `gpt-4`). This allows for easy switching between different LLM versions or other language models. The `pg.TextLLM` interface plays a central role in achieving this independence. Through this interface, users can inject their own LLM implementations into PromptoGen.

Thus, through the `pg.TextLLM` interface, PromptoGen retains flexibility and extensibility.

## About `TextLLM`

The `TextLLM` abstract class is an interface for Large Language Models (LLM) that generate text from text.

`TextLLM` has a `generate` method. This method takes in text and returns text.

```python title="Reference: text_llm.py"
class LLM(ABC):
    """Language model interface."""

    pass

class TextLLM(LLM, ABC):
    """Language model interface that generates text from text."""

    @abstractmethod
    def generate(self, input_text: str) -> str:
        pass
```

Promptogen is designed to not depend on a specific LLM. `TextLLM` is a prime example of this. By defining such interfaces, various large language models can be handled uniformly.

## Implementation Example 1: Using a Custom Class

For instance, here's an example of implementing `TextLLM` using the OpenAI API. You can define a function like `generate_chat_completion` as shown below.

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

By inheriting from the `TextLLM` class, you can implement `TextLLM`.

```python
import promptogen as pg

class OpenAITextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_chat_completion(text, self.model)
```

## Implementation Example 2: Implementing `TextLLM` based on a Function

The `FunctionBasedTextLLM` class is one implementation of Large Language Models (LLM) that generate text from text.

By specifying a function of the form `(input_text: str) -> str`, you can implement `TextLLM`.

Compared to creating a custom class, you can implement `TextLLM` more simply.

```python
text_llm = FunctionBasedTextLLM(
    generate_text_by_text=lambda input_text: generate_chat_completion(input_text, "gpt-3.5-turbo"),
)
```

## How to Use

```python
text_llm = OpenAITextLLM("gpt-3.5-turbo")

print(text_llm.generate("Hello, I'm a human."))
# Hello! How can I assist you today as an AI?
```

Essentially, by building implementations that rely on `pg.TextLLM`, it becomes easier to construct a **generic system that doesn't depend on any specific LLM**.
