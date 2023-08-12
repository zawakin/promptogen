このページでは、既存のプロンプトを、推論を出力するように変換する方法を説明します。

`openai_util.OpenAITextLLM` は[OpenAITextLLMページ](openai-text-llm.md) で定義した `TextLLM` です（参考: [TextLLM](../getting-started/text-llm.md)）。
同じディレクトリの `openai_util.py` にそれらを定義しておくと、`import` できます。

`PromptWithReasoningTransformer` は、プロンプトの出力に推論を追加するための `PromptTransformer` です。

`PromptTransformer`抽象クラスは、プロンプトからプロンプトを生成するためのクラスです。

```python
class PromptTransformer(ABC):
    """Transform a prompt. This is useful for various purposes, such as:
    - Adding reasoning output parameters to the prompt.
    - Adding examples to the prompt.
    - etc.
    """

    @abstractmethod
    def transform_prompt(self, prompt: Prompt) -> Prompt:
        pass
```

`PromptWithReasoningTransformer` は `(arg1, arg2, ..., argN) -> (ret1, ret2, ..., retM)` というプロンプトの出力を `(arg1, arg2, ..., argN) -> (reasoning, ret1, ret2, ..., retM)` という形に変換します。

オリジナルプロンプトの `IOExample` に対する推論過程の出力を `TextLLMReasoningExtractor` で生成します([詳細](context-qa-reasoning.md))。


```python
import promptogen as pg
from openai_util import OpenAITextLLM
from promptogen.prompt_collection import PromptCreatorPrompt
from promptogen.prompt_tool import TextLLMReasoningExtractor

llm = OpenAITextLLM(model="gpt-3.5-turbo")

formatter = pg.KeyValuePromptFormatter()
prompt_runner = pg.TextLLMPromptRunner(llm=llm, formatter=formatter)

prompt_creator_prompt = PromptCreatorPrompt()


def setup_context_qa_prompt() -> pg.Prompt:
    input_value = {
        "description": "Answer the question for the given context.",
        "background": "(context: str, question: str) -> (answer: str)",
    }
    resp = prompt_runner.run_prompt(prompt_creator_prompt, input_value=input_value)
    return pg.Prompt.from_dict(resp["prompt"])


context_qa_prompt = setup_context_qa_prompt()
print(context_qa_prompt)
# ContextualQuestionAnswering: (context: str, question: str) -> (answer: str)

# Description
# -----------
# Answer the question for the given context.

# Input Parameters
# ----------------
# - context (str): The contextual information
# - question (str): The question based on the context

# Output Parameters
# -----------------
# - answer (str): The answer to the question

# Examples Count
# --------------
# 1

from promptogen.prompt_tool import PromptWithReasoningTransformer

reasoning_extractor = TextLLMReasoningExtractor(
    text_llm=llm,
    reasoning_template="This is because ... So the answer is ...",
)
transformer = PromptWithReasoningTransformer(reasoning_extractor=reasoning_extractor)

context_qa_prompt_with_reasoning = transformer.transform_prompt(context_qa_prompt)
print(context_qa_prompt_with_reasoning)
# ContextualQuestionAnswering: (context: str, question: str) -> (reasoning: str, answer: str)

# Description
# -----------
# Answer the question for the given context.

# Input Parameters
# ----------------
# - context (str): The contextual information
# - question (str): The question based on the context

# Output Parameters
# -----------------
# - reasoning (str): Reasoning for the output
# - answer (str): The answer to the question

# Examples Count
# --------------
# 1

input_value = {
    "context": "The quick brown fox jumps over the lazy dog.",
    "question": "What does the fox jump over?",
}

output_value = prompt_runner.run_prompt(context_qa_prompt_with_reasoning, input_value=input_value)
print(output_value)
# {'reasoning': 'This is because the context provides information that the quick brown fox jumps over the lazy dog. The question asks what the fox jumps over. Therefore, the answer is that the fox jumps over the lazy dog.', 'answer': 'The fox jumps over the lazy dog.'}

```
