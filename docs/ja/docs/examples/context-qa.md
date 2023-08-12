このページでは、コンテキストと質問を入力として受け取り、回答を出力するプロンプトを作成する方法を説明します。

## 準備

`openai_util.OpenAITextLLM` は[OpenAITextLLMページ](openai-text-llm.md) で定義した `TextLLM` です（参考: [TextLLM](../getting-started/text-llm.md)）。
同じディレクトリの `openai_util.py` にそれらを定義しておくと、`import` できます。

```python
import promptogen as pg
from openai_util import OpenAITextLLM
from promptogen.prompt_collection import PromptCreatorPrompt

llm = OpenAITextLLM(model="gpt-3.5-turbo")

formatter = pg.KeyValuePromptFormatter()
prompt_runner = pg.TextLLMPromptRunner(llm=llm, formatter=formatter)

```

## プロンプトの作成

`PromptCreatorPrompt` を使用して、プロンプトを作成します。

このプロンプトは　`description` と `background` を入力として受け取り、`prompt` を出力します。

```python
prompt_creator_prompt = PromptCreatorPrompt()


def setup_context_qa_prompt() -> pg.Prompt:
    input_value = {
        "description": "Answer the question for the given context.",
        "background": "(context: str, question: str) -> (answer: str)",
    }
    resp = prompt_runner.run_prompt(prompt_creator_prompt, input_value=input_value)
    return pg.Prompt.from_dict(resp["prompt"])


context_qa_prompt = setup_context_qa_prompt()
```

LLMへの入力:

```console
-- input --
Create a prompt from the given description and background. Use the given description as the prompt description as is. Consider background information to make the prompt more specific.

Input Parameters:
  - description: description of the prompt; this will be used as the prompt description as is
  - background: background of the prompt

Output Parameters:
  - prompt: A prompt which has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.

Template:
Input:
description: "description of sample prompt"
background: "background of the prompt"
Output:
prompt: { 'name': 'sample-new prompt',
  'description': 'description of sample prompt',
  'input_parameters': [{'name': 'input1', 'description': 'The first input parameter.'}, {'name': 'input2', 'description': 'The second input parameter.'}],
  'output_parameters': [{'name': 'output1', 'description': 'The first output parameter.'}, {'name': 'output2', 'description': 'The second output parameter.'}],
  'template': {'input': {'input1': 'Hello, world!', 'input2': 'Hello, world!'}, 'output': {'output1': 'Hello, world!', 'output2': 'Hello, world!'}},
  'examples': [ {'input': {'input1': 'Hello, world!', 'input2': 'Hello, world!'}, 'output': {'output1': 'Hello, world!', 'output2': 'Hello, world!'}},
                {'input': {'input1': 'Hello, world!', 'input2': 'Hello, world!'}, 'output': {'output1': 'Hello, world!', 'output2': 'Hello, world!'}}]}

Example 1:
Input:
description: "Categorize the given text"
background: "The given text may be a sentence, a paragraph, or a document."
Output:
prompt: { 'name': 'TextCategorizer',
  'description': 'Categorize the given text',
  'input_parameters': [ {'name': 'text', 'description': 'The text to be categorized'},
                        {'name': 'categories', 'description': 'The categories to categorize the text into'}],
  'output_parameters': [{'name': 'category', 'description': 'The category the text belongs to'}],
  'template': {'input': {'text': 'text', 'categories': ['category 1', 'category 2']}, 'output': {'category': 'category 1'}},
  'examples': [ { 'input': { 'text': 'A recent study shows that regular exercise can help improve cognitive function in older adults.',
                             'categories': ['Health', 'Science', 'Technology']},
                  'output': {'category': 'Health'}}]}

Example 2:
Input:
description: "Generate Python code based on the given task"
background: "style: input: (task: str), output: (reason: str, code: str)"
Output:
prompt: { 'name': 'PythonCodeGenerator',
  'description': 'Generate Python code based on the given task',
  'input_parameters': [{'name': 'task', 'description': 'The task for which Python code needs to be generated'}],
  'output_parameters': [ {'name': 'reason', 'description': 'Reason for the generated Python code'},
                         {'name': 'code', 'description': 'Python code generated to complete the task'}],
  'template': {'input': {'task': 'task'}, 'output': {'reason': 'reason', 'code': 'code'}},
  'examples': [ { 'input': {'task': 'Create a function that calculates the factorial of a number'},
                  'output': { 'reason': 'Factorial function is a common use case in Python programming',
                              'code': 'def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)'}}]}

--------

Input:
description: "Answer the question for the given context."
background: "(context: str, question: str) -> (answer: str)"
Output:

```

LLMからの出力:

```console
-- output --
prompt: { 'name': 'ContextQuestionAnswer',
  'description': 'Answer the question for the given context.',
  'input_parameters': [{'name': 'context', 'description': 'The context in which the question is asked'},
                       {'name': 'question', 'description': 'The question to be answered'}],
  'output_parameters': [{'name': 'answer', 'description': 'The answer to the given question'}],
  'template': {'input': {'context': 'context', 'question': 'question'}, 'output': {'answer': 'answer'}},
  'examples': [ {'input': {'context': 'In 1956, John McCarthy coined the term "Artificial Intelligence" at the Dartmouth Conference.',
                           'question': 'Who coined the term "Artificial Intelligence" and when?'}, 
                 'output': {'answer': 'John McCarthy coined the term "Artificial Intelligence" in 1956.'}}]}
```

## 作成したプロンプト情報の確認

```python
print(context_qa_prompt)
```

```console
ContextQuestionAnswer: (context: str, question: str) -> (answer: str)

Description
-----------
Answer the question for the given context.

Input Parameters
----------------
- context (str): The context in which the question is asked
- question (str): The question to be answered

Output Parameters
-----------------
- answer (str): The answer to the given question

Examples Count
--------------
1
```

## Context QA プロンプトの実行

Context QA プロンプトを実行してみます。

```python
input_value = {
    "context": "The quick brown fox jumps over the lazy dog.",
    "question": "What does the fox jump over?",
}

output_value = prompt_runner.run_prompt(context_qa_prompt, input_value=input_value)

print(output_value["answer"])
# -> The fox jumps over the lazy dog.
```

LLMへの入力:

```console
-- input --
Answer the question for the given context.

Input Parameters:
  - context: The context in which the question is asked
  - question: The question to be answered

Output Parameters:
  - answer: The answer to the given question

Template:
Input:
context: "context"
question: "question"
Output:
answer: """answer"""

Example 1:
Input:
context: "In 1956, John McCarthy coined the term \"Artificial Intelligence\" at the Dartmouth Conference."
question: "Who coined the term \"Artificial Intelligence\" and when?"
Output:
answer: """John McCarthy coined the term \"Artificial Intelligence\" in 1956."""

--------

Input:
context: "The quick brown fox jumps over the lazy dog."
question: "What does the fox jump over?"
Output:

```

LLMからの出力:

```console
-- output --
answer: """The fox jumps over the lazy dog."""
```

