In [Context QA](context-qa.md), we created a prompt to answer questions based on a given context. Based on this prompt, not only can we generate answers to questions, but we can also use a given set of input and output to generate the reasoning process that derives the output from the input.

To generate such reasoning, use `TextLLMReasoningExtractor`.

## Source Code

[context-qa.py (GitHub)](https://github.com/zawakin/promptogen/tree/742485c4690788d2866635bcd3b5eda580cf5b1a/examples/promptcreation/context_qa_prompt.py)

## Setup

`openai_util.OpenAITextLLM` is the `TextLLM` defined on the [OpenAITextLLM page](openai-text-llm.md) (refer to: [TextLLM](../getting-started/text-llm.md)). If you define them in the same directory's `openai_util.py`, you can `import` them.

```python
import promptogen as pg
from promptogen.prompt_tool import TextLLMReasoningExtractor

from openai_util import OpenAITextLLM

llm = OpenAITextLLM(model="gpt-3.5-turbo")

```

## Running the Context QA Prompt (Reasoning)

Suppose you have the following input and output:

```python
Input:
context: "The quick brown fox jumps over the lazy dog."
question: "What does the fox jump over?"

Output:
answer: "The fox jumps over the lazy dog."
```

You can generate the reasoning process for producing the `answer` from the given `(context, question)` pair.

Specify the template for generating reasoning in `reasoning_template`.

Pass the instance of the `Prompt` class and the set of input-output to the `generate_reasoning` method.

`context_qa_prompt` is the prompt created in [Context QA](context-qa.md).

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
    "answer": "The lazy dog.",
}
example = pg.IOExample(
    input=input_value,
    output=output_value,
)
reasoning = reasoning_extractor.generate_reasoning(context_qa_prompt, example)
print(reasoning)
```

LLM Input:

```console
-- input --
Please detail the cause-and-effect relationship that begins with the inputs (context: str, question: str) and leads to the outputs (answer: str), outlining the reasoning process from the initial inputs to the final outputs.

Template:
Input:
context: "context"
question: "question"
answer: "Answer"
Output:
This is because ... So the answer is ...
--------

Input:
context: "The quick brown fox jumps over the lazy dog."
question: "What does the fox jump over?"
answer: "The lazy dog."
Output:
```

LLM Output:

```console
-- output --
This is because the question is asking what the fox jumps over. To determine the answer, we need to look at the context. In the context, it is stated that the quick brown fox jumps over the lazy dog. Therefore, the answer is "The lazy dog."
```

Following the template "This is because ... So the answer is ...", the reasoning process was generated.
