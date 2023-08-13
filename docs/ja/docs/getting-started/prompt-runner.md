`PromptRunner` は、プロンプトを `TextLLM` を通じて実行するためのインターフェースです。

`PromptRunner` は `run_prompt` メソッドを持ちます。このメソッドは、プロンプトと入力を受け取り、出力を `Value` (つまり `dict` )にパースした結果を返します。

```python
class PromptRunner(ABC):
    """A prompt runner is responsible for running a prompt and returning the result."""

    @abstractmethod
    def run_prompt(self, prompt: Prompt, input_value: Value) -> Value:
        pass
```

## 例: TextLLMPromptRunner

`TextLLMPromptRunner` によるプロンプトの実行は、以下の手順で行われます。

1. `PromptFormatter` を使用して、プロンプトと入力値をテキストにフォーマットします。
2. `TextLLM` を使用して、テキストを生成します。
3. `PromptFormatter` を使用して、生成されたテキストを解析して、`Value` を返します。

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

## 使い方

ここでは、 `TextLLM`には[TextLLM](text-llm.md)で例を出した `OpenAITextLLM` クラスを使用します。

また、実行するプロンプトは [Prompt](prompt.md) で作成した `summarizer` プロンプトを使用します。

```python
import promptogen as pg

class OpenAITextLLM(pg.TextLLM):
    # 省略

text_llm = OpenAITextLLM("gpt-3.5-turbo")
formatter = pg.KeyValuePromptFormatter()

runner = pg.TextLLMPromptRunner(text_llm, formatter)

input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.",
}
resp = runner.run_prompt(summarizer, input_value)
print(resp)
# {'summary': 'Software developers collaborate using version control systems like Git to create and maintain efficient code and solve implementation and optimization issues.', 'keywords': ['software engineering', 'developers', 'collaborate', 'projects', 'version control systems', 'Git', 'code', 'implementation complexities', 'evolving user requirements', 'system optimization']}
```

