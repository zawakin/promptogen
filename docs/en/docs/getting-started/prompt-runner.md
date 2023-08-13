`PromptRunner` is an interface for executing prompts through `TextLLM`.

`PromptRunner` possesses a `run_prompt` method. This method takes a prompt and input, then returns the output parsed into a `Value` (which is essentially a `dict`).

```python
class PromptRunner(ABC):
    """A prompt runner is responsible for running a prompt and returning the result."""

    @abstractmethod
    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        pass
```

## Example: TextLLMPromptRunner

The execution of a prompt by `TextLLMPromptRunner` follows these steps:

1. Use `PromptFormatter` to format the prompt and input values into text.
2. Utilize `TextLLM` to generate the text.
3. Employ `PromptFormatter` to analyze the generated text and return the `Value`.

```python
class TextLLMPromptRunner(PromptRunner):
    """A text-based prompt runner is responsible for running a prompt and returning the result."""

    def __init__(self, llm: TextLLM, formatter: PromptFormatter):
        """Initialize a TextBasedPromptRunner.

        Args:
            llm: The LLM to use. It must be an instance of TextBasedLLM.
            formatter: The prompt formatter to use. It must be an instance of PromptFormatter.
        """
        self.text_llm = llm
        self.formatter = formatter

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

## How to Use

In this example, the `TextLLM` class we'll use is `OpenAITextLLM`, as mentioned in the [TextLLM](text-llm.md) example. 

Additionally, the prompt to execute is the `summarizer` prompt, as created in the [Prompt](prompt.md).

```python
import promptogen as pg

text_llm = pg.OpenAITextLLM("gpt-3.5-turbo")
formatter = pg.KeyValuePromptFormatter()

runner = pg.TextLLMPromptRunner(text_llm, formatter)

input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.",
}
resp = runner.run_prompt(summarizer, input_value)
print(resp)
# {'summary': 'Software developers collaborate using version control systems like Git to create and maintain efficient code and solve implementation and optimization issues.', 'keywords': ['software engineering', 'developers', 'collaborate', 'projects', 'version control systems', 'Git', 'code', 'implementation complexities', 'evolving user requirements', 'system optimization']}
```
