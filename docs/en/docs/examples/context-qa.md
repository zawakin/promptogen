This page explains how to create a prompt that takes a context and a question as input and outputs an answer.

## Setup

`openai_util.OpenAITextLLM` is the `TextLLM` defined on the [OpenAITextLLM page](openai-text-llm.md) (see also: [TextLLM](../getting-started/text-llm.md)). If you define them in the same directory's `openai_util.py`, you can `import` them.

```python
import promptogen as pg
from openai_util import OpenAITextLLM
from promptogen.prompt_collection import PromptCreatorPrompt

llm = OpenAITextLLM(model="gpt-3.5-turbo")

formatter = pg.KeyValuePromptFormatter()
prompt_runner = pg.TextLLMPromptRunner(llm=llm, formatter=formatter)

```

## Source Code

[context-qa.py (GitHub)](https://github.com/zawakin/promptogen/tree/742485c4690788d2866635bcd3b5eda580cf5b1a/examples/promptcreation/context_qa_prompt.py)

## Creating the Prompt

Using `PromptCreatorPrompt`, we will create a prompt.

This prompt takes `description` and `background` as input and outputs `prompt`.

```python
prompt_creator_prompt = PromptCreatorPrompt()

def setup_context_qa_prompt() -> pg.Prompt:
    input_value = {
        "description": "Answer the question based on the given context.",
        "background": "(context: str, question: str) -> (answer: str)",
    }
    resp = prompt_runner.run_prompt(prompt_creator_prompt, input_value=input_value)
    return pg.Prompt.from_dict(resp["prompt"])

context_qa_prompt = setup_context_qa_prompt()
```

Input to LLM:

```console
-- input --
Create a prompt from the given description and background. Use the provided description as the prompt's description directly. Use background information to make the prompt more specific.

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
prompt: {
 "name": "sample-new prompt",
 "description": "description of sample prompt",
 "input_parameters": [
  {
   "name": "input1",
   "description": "The first input parameter."
  },
  {
   "name": "input2",
   "description": "The second input parameter."
  }
 ],
 "output_parameters": [
  {
   "name": "output1",
   "description": "The first output parameter."
  },
  {
   "name": "output2",
   "description": "The second output parameter."
  }
 ],
 "template": {
  "input": {
   "input1": "Hello, world!",
   "input2": "Hello, world!"
  },
  "output": {
   "output1": "Hello, world!",
   "output2": "Hello, world!"
  }
 },
 "examples": [
  {
   "input": {
    "input1": "Hello, world!",
    "input2": "Hello, world!"
   },
   "output": {
    "output1": "Hello, world!",
    "output2": "Hello, world!"
   }
  },
  {
   "input": {
    "input1": "Hello, world!",
    "input2": "Hello, world!"
   },
   "output": {
    "output1": "Hello, world!",
    "output2": "Hello, world!"
   }
  }
 ]
}

Example 1:
Input:
description: "Categorize the given text"
background: "The given text may be a sentence, a paragraph, or a document."
Output:
prompt: {
 "name": "TextCategorizer",
 "description": "Categorize the given text",
 "input_parameters": [
  {
   "name": "text",
   "description": "The text to be categorized"
  },
  {
   "name": "categories",
   "description": "The categories to categorize the text into"
  }
 ],
 "output_parameters": [
  {
   "name": "category",
   "description": "The category the text belongs to"
  }
 ],
 "template": {
  "input": {
   "text": "text",
   "categories": [
    "category 1",
    "category 2"
   ]
  },
  "output": {
   "category": "category 1"
  }
 },
 "examples": [
  {
   "input": {
    "text": "A recent study shows that regular exercise can help improve cognitive function in older adults.",
    "categories": [
     "Health",
     "Science",
     "Technology"
    ]
   },
   "output": {
    "category": "Health"
   }
  }
 ]
}

Example 2:
Input:
description: "Generate Python code based on the given task"
background: "style: input: (task: str), output: (reason: str, code: str)"
Output:
prompt: {
 "name": "PythonCodeGenerator",
 "description": "Generate Python code based on the given task",
 "input_parameters": [
  {
   "name": "task",
   "description": "The task for which Python code needs to be generated"
  }
 ],
 "output_parameters": [
  {
   "name": "reason",
   "description": "Reason for the generated Python code"
  },
  {
   "name": "code",
   "description": "Python code generated to complete the task"
  }
 ],
 "template": {
  "input": {
   "task": "task"
  },
  "output": {
   "reason": "reason",
   "code": "code"
  }
 },
 "examples": [
  {
   "input": {
    "task": "Create a function that calculates the factorial of a number"
   },
   "output": {
    "reason": "Factorial function is a common use case in Python programming",
    "code": "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)"
   }
  }
 ]
}

--------

Input:
description: "Answer the question based on the given context."
background: "(context: str, question: str) -> (answer: str)"
Output:
```

Output from LLM:

```console
-- output --
prompt: {
 "name": "QuestionAnswering",
 "description": "Answer the question for the given context.",
 "input_parameters": [
  {
   "name": "context",
   "description": "The context in which the question needs to be answered"
  },
  {
   "name": "question",
   "description": "The question to be answered"
  }
 ],
 "output_parameters": [
  {
   "name": "answer",
   "description": "The answer to the question from the given context"
  }
 ],
 "template": {
  "input": {
   "context": "context",
   "question": "question"
  },
  "output": {
   "answer": "Answer"
  }
 },
 "examples": [
  {
   "input": {
    "context": "The Apollo program, also known as Project Apollo, was the third United States human spaceflight program carried out by the National Aeronautics and Space Administration (NASA), which succeeded in landing the first humans on the Moon from 1969 to 1972.",
    "question": "Which organization carried out the Apollo program?"
   },
   "output": {
    "answer": "National Aeronautics and Space Administration (NASA)"
   }
  }
 ]
}
```

## Verifying the Created Prompt Information

```python
print(context_qa_prompt)
```

```console
QuestionAnswering: (context: str, question: str) -> (answer: str)

Description
-----------
Answer the question based on the given context.

Input Parameters
----------------
- context (str): The context in which the question needs to be answered
- question (str): The question to be answered

Output Parameters
-----------------
- answer (str): The answer to the question from the given context

Examples Count
--------------
1
```

## Running the Context QA Prompt

Let's run the Context QA prompt.

```python
input_value = {
    "context": "The quick brown fox jumps over the lazy dog.",
    "question": "What does the fox jump over?",
}

output_value = prompt_runner.run_prompt(context_qa_prompt, input_value=input_value)

print(output_value["answer"])
# -> The lazy dog.
```

Input to LLM:

```console
-- input --
Answer the question based on the given context.

Input Parameters:
  - context: The context in which the question needs to be answered
  - question: The question to be answered

Output Parameters:
  - answer: The answer to the question from the given context

Template:
Input:
context: "context"
question: "question"
Output:
answer: """Answer"""

Example 1:
Input:
context: "The Apollo program, also known as Project Apollo, was the third United States human spaceflight program carried out by the National Aeronautics and Space Administration (NASA), which succeeded in landing the first humans on the Moon from 1969 to 1972."
question: "Which organization carried out the Apollo program?"
Output:
answer: """National Aeronautics and Space Administration (NASA)"""

--------

Input:
context: "The quick brown fox jumps over the lazy dog."
question: "What does the fox jump over?"
Output:
```

Output from LLM:

```console
-- output --
answer: """The lazy dog."""
```
