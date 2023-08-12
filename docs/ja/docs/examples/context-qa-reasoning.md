[Context QA](context-qa.md) では、与えられたコンテキストに対して質問に答えるプロンプトを作成しました。
このプロンプトを元に、質問に対する答えを生成するだけでなく、ある与えられた入力と出力の組を用いて、入力から出力を導く推論過程を生成することもできます。

そのような推論を生成するためには、 `TextLLMReasoningExtractor` を使用します。

## 準備

`openai_util.OpenAITextLLM` は[OpenAITextLLMページ](openai-text-llm.md) で定義した `TextLLM` です（参考: [TextLLM](../getting-started/text-llm.md)）。
同じディレクトリの `openai_util.py` にそれらを定義しておくと、`import` できます。

```python
import promptogen as pg
from promptogen.prompt_tool import TextLLMReasoningExtractor

from openai_util import OpenAITextLLM

llm = OpenAITextLLM(model="gpt-3.5-turbo")

```

## Context QA プロンプトの実行 (Reasoning)

もし、以下のような入出力があったとします。

```python
Input:
context: "The quick brown fox jumps over the lazy dog."
question: "What does the fox jump over?"

Output:
answer: "The fox jumps over the lazy dog."
```

`(context, question)` の組が与えられたときに `answer` を生成する推論過程を生成することができます。


`reasoning_template` には、推論を生成するためのテンプレートを指定します。

`generate_reasoning` メソッドには、 `Prompt` クラスのインスタンスと、入出力の組を与えます。

`context_qa_prompt` は、[Context QA](context-qa.md) で作成したプロンプトです。

```python
reasoning_extractor = TextLLMReasoningExtractor(
    text_llm=llm,
    reasoning_template="This is because ... So the answer is ...",
)

input_value = {
    "context": "The quick brown fox jumps over the lazy dog.",
    "question": "What does the fox jump over?",
}
output_value = {
    "answer": "The fox jumps over the lazy dog.",
}
example = pg.IOExample(
    input=input_value,
    output=output_value,
)
reasoning = reasoning_extractor.generate_reasoning(context_qa_prompt, example)
print(reasoning)
```

LLM入力:

```console
-- input --
Please detail the cause-and-effect relationship that begins with the inputs (context: str, question: str) and leads to the outputs (answer: str), outlining the reasoning process from the initial inputs to the final outputs.

Template:
Input:
context: "context"
question: "question"
answer: "answer"
Output:
This is because ... So the answer is ...
--------

Input:
context: "The quick brown fox jumps over the lazy dog."
question: "What does the fox jump over?"
answer: "The fox jumps over the lazy dog."
Output:
```

LLM出力:

```console
-- output --
This is because the context provided states that "The quick brown fox jumps over the lazy dog." The question asks "What does the fox jump over?" The answer can be derived from the context, as it explicitly states that the fox jumps over the lazy dog. So the answer is "The fox jumps over the lazy dog."
```

`"This is because ... So the answer is ..."` というテンプレートに従って、推論過程が生成されました。
