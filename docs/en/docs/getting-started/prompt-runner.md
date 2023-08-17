## PromptRunner: Simplifying Prompt Execution

`pg.PromptRunner` is a core component of PromptoGen, serving the purpose of efficiently executing prompts created by users. Its prime feature is the ability to **run prompts without having to be concerned about the specifics of the LLM (Large Language Model) implementation**. This significantly simplifies the creation and management of prompts.

### Usage Example

```python
import promptogen as pg

# formatter is an object that formats prompts
formatter = pg.KeyValuePromptFormatter()

# For the creation of a TextLLM instance, refer to the `TextLLM` page
runner = pg.TextLLMPromptRunner(llm=text_llm, formatter=formatter)

# Creating an actual prompt
summarizer = pg.Prompt(
    name="Text Summarizer and Keyword Extractor",
    # ...
)

# Running the prompt
input_value = {
    "text": "In the realm of software engineering, ...",
}
output_value = runner.run_prompt(summarizer, input_value)
print(output_value)
```

## Why is `pg.PromptRunner` useful?

1. **Abstraction**: Users can execute prompts without being aware of the specifics of the LLM implementation.
2. **Consistency**: Makes changes minimal when running the same prompt using different LLMs.
3. **Extensibility**: Easy to add new prompts or modify existing ones.

Thus, `pg.PromptRunner` is a potent tool in PromptoGen for executing prompts efficiently and conveniently.

## Overview of `PromptRunner`

Users select the desired `TextLLM` and `PromptFormatter` and create a `PromptRunner`.

By providing the `Prompt` and `InputValue` to the `PromptRunner`, you can obtain the `OutputValue`.

- Input to `PromptRunner`: `Prompt` and `InputValue`
- Output from `PromptRunner`: `OutputValue`

`PromptRunner` operates in the following sequence:

1. Receives `Prompt` and `InputValue`
2. Generates a prompt string
3. Passes the generated prompt string to `TextLLM`
4. Receives output from `TextLLM`
5. Converts the output to `OutputValue` using `PromptFormatter`
6. Returns `OutputValue`

![Overview of PromptoGen](../img/promptogen_overview.png)

## `pg.PromptRunner` Interface

`PromptRunner` has a `run_prompt` method. This method receives a prompt and input and returns the output parsed to `Value` (i.e., `dict`).

```python title="Reference: Abstract class for PromptRunner"
class PromptRunner(ABC):
    @abstractmethod
    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        pass
```

## `pg.TextLLMPromptRunner` Implementation

The execution of prompts using `pg.TextLLMPromptRunner` is performed as follows:

1. Use the `PromptFormatter` to format the prompt and input values into text.
2. Generate text using `TextLLM`.
3. Parse the generated text using `PromptFormatter` to return a `Value`.

```python title="Reference: Implementation of TextLLMPromptRunner"
class TextLLMPromptRunner(PromptRunner):
    # ...

    def __init__(self, llm: TextLLM, formatter: PromptFormatter):
        self.text_llm = llm
        self.formatter = formatter

    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        raw_req = self.formatter.format_prompt(prompt, input_value)
        raw_resp = self.text_llm.generate(raw_req)
        resp = self.formatter.parse(prompt, raw_resp)
        return resp
```

## Usage

Here, we use the `OpenAITextLLM` class introduced in the [TextLLM](text-llm.md) example for `TextLLM`.

Moreover, for the prompt to be executed, we use the `summarizer` prompt created in [Prompt](prompt.md).

```python
import promptogen as pg

class OpenAITextLLM(pg.TextLLM):
    # ...(omitted)...

text_llm = OpenAITextLLM("gpt-3.5-turbo")
formatter = pg.KeyValuePromptFormatter()

runner = pg.TextLLMPromptRunner(text_llm, formatter)

input_value = {
    'text': "In the realm of software engineering, ...",
}
resp = runner.run_prompt(summarizer, input_value)
print(resp)
# {'summary': 'Software developers collaborate ...', 'keywords': ['software engineering', 'developers', ...]}
```
