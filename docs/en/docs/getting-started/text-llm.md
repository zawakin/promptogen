The `TextLLM` abstract class is an interface for Large Language Models (LLM) that generate text from text.

`TextLLM` has a `generate` method. This method takes text as input and returns text.

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

Promptogen is designed to be independent of any specific LLM. `TextLLM` is a prime example of this. By defining such interfaces, various large language models can be handled uniformly.

## Method 1: Implementation using a custom class

### Example using the OpenAI API

Here is an example of implementing `TextLLM` using the OpenAI API. For instance, you can define a function called `generate_chat_completion` as follows:

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

By inheriting the `TextLLM` class, you can implement `TextLLM`.

```python
import promptogen as pg

class OpenAITextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_chat_completion(text, self.model)
```

## Method 2: FunctionBasedTextLLM

The `FunctionBasedTextLLM` class is one of the implementations of the Large Language Model (LLM) that generates text from text.

By specifying a function of the form `(input_text: str) -> str`, you can implement `TextLLM`.

Compared to creating a custom class, this allows you to implement `TextLLM` more easily.

```python
text_llm = FunctionBasedTextLLM(
    generate_text_by_text=lambda input_text: generate_chat_completion(input_text, "gpt-3.5-turbo"),
)
```

## How to use

```python
text_llm = OpenAITextLLM("gpt-3.5-turbo")

print(text_llm.generate("Hello, I'm a human."))
# Hello! How can I assist you today as an AI?
```
