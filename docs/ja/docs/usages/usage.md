# 使い方

```python
import promptgen as pg
```


```python
collection = pg.PromptCollection(load_predefined=True)

```

## Setup for LLM (OpenAI ChatGPT API here)


```python
from colorama import Fore

import openai
import os

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

def completion(prompt: str, model: str):
        resp = openai.ChatCompletion.create(model=model, messages=[
            {'role': 'user', 'content': prompt}
        ], stream=True, max_tokens=2048)
        for chunk in resp:
            yield chunk['choices'][0]['delta'].get('content', '')

def get_llm_response(prompt: str, model: str = 'gpt-3.5-turbo'):
    s = ''
    print(Fore.LIGHTBLACK_EX)
    for delta in completion(prompt, model):
        print(delta, end='')
        s += delta
    print(Fore.BLACK)
    return s
```


```python
formatter = pg.KeyValuePromptFormatter()

def run(prompt: pg.Prompt, input_value: pg.InputValue) -> pg.OutputValue:
    raw_req = formatter.format_prompt(prompt=prompt, input_value=input_value)
    raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')
    return formatter.parse(raw_resp)
```


```python
prompt_creator = collection['PromptCreator']

prompt_creator
```




```json
{
    "name": "PromptCreator",
    "description": "Create a prompt from the given purpose. Don't create an example with the input purpose. Instead, create an example with a different purpose. Consider background information that is necessary to understand the purpose.",
    "input_parameters": [
        {
            "name": "purpose",
            "description": "purpose of the prompt"
        },
        {
            "name": "background",
            "description": "background of the prompt"
        }
    ],
    "output_parameters": [
        {
            "name": "prompt",
            "description": "prompt created from the given purpose. Is has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'."
        }
    ],
    "template": {
        "input": {
            "purpose": "purpose of the prompt",
            "background": "background of the prompt"
        },
        "output": {
            "prompt": {
                "name": "sample-new prompt",
                "description": "A sample prompt.",
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
        }
    },
    "examples": [
        {
            "input": {
                "purpose": "Categorize the given text into one of the given categories.",
                "background": "The given text may be a sentence, a paragraph, or a document."
            },
            "output": {
                "prompt": {
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
                        },
                        {
                            "name": "found",
                            "description": "Whether the category was found in the text"
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
                            "category": "category 1",
                            "found": true
                        }
                    },
                    "examples": []
                }
            }
        },
        {
            "input": {
                "purpose": "Summarize the given text.",
                "background": "The given text may be the part of the document."
            },
            "output": {
                "prompt": {
                    "name": "TextSummarizer",
                    "description": "Summarize the text into a shorter text.",
                    "input_parameters": [
                        {
                            "name": "text",
                            "description": "text to summarize"
                        }
                    ],
                    "output_parameters": [
                        {
                            "name": "summary",
                            "description": "summary of the text"
                        }
                    ],
                    "template": {
                        "input": {
                            "text": "text"
                        },
                        "output": {
                            "summary": "summary"
                        }
                    },
                    "examples": []
                }
            }
        }
    ]
}
```




```python

resp = run(prompt_creator, pg.InputValue(purpose='Split a task into subtasks', background='style: (task: str) -> (reason: str, subtasks: list[str])'))
```

```
prompt: {'name': 'TaskSplitter', 'description': 'Split a task into subtasks', 'input_parameters': [{'name': 'task', 'description': 'Task to be split into subtasks'}], 'output_parameters': [{'name': 'reason', 'description': 'Reason for splitting the task'}, {'name': 'subtasks', 'description': 'List of subtasks after splitting the task'}], 'template': {'input': {'task': 'task'}, 'output': {'reason': 'reason', 'subtasks': ['subtask 1', 'subtask 2'] }}, 'examples': [{'input': {'task': 'Write a research paper'}, 'output': {'reason': 'To make it more manageable.', 'subtasks': ['Research the topic', 'Gather sources', 'Write a draft', 'Revise and Edit', 'Format the paper'] }}, {'input': {'task': 'Plan a vacation'}, 'output': {'reason': 'To plan more effectively.', 'subtasks': ['Decide on a location', 'Determine a budget', 'Book travel arrangements', 'Plan activities'] }}]}
```



```python
task_splitter = pg.load_prompt_from_dict(resp.prompt)
task_splitter
```




    {
        "name": "TaskSplitter",
        "description": "Split a task into subtasks",
        "input_parameters": [
            {
                "name": "task",
                "description": "Task to be split into subtasks"
            }
        ],
        "output_parameters": [
            {
                "name": "reason",
                "description": "Reason for splitting the task"
            },
            {
                "name": "subtasks",
                "description": "List of subtasks after splitting the task"
            }
        ],
        "template": {
            "input": {
                "task": "task"
            },
            "output": {
                "reason": "reason",
                "subtasks": [
                    "subtask 1",
                    "subtask 2"
                ]
            }
        },
        "examples": [
            {
                "input": {
                    "task": "Write a research paper"
                },
                "output": {
                    "reason": "To make it more manageable.",
                    "subtasks": [
                        "Research the topic",
                        "Gather sources",
                        "Write a draft",
                        "Revise and Edit",
                        "Format the paper"
                    ]
                }
            },
            {
                "input": {
                    "task": "Plan a vacation"
                },
                "output": {
                    "reason": "To plan more effectively.",
                    "subtasks": [
                        "Decide on a location",
                        "Determine a budget",
                        "Book travel arrangements",
                        "Plan activities"
                    ]
                }
            }
        ]
    }




```python
class TaskSplitterInput(pg.InputValue):
    task: str

class TaskSplitterOutput(pg.OutputValue):
    reason: str
    subtasks: list[str]
```


```python
resp = run(task_splitter, TaskSplitterInput(task='write a book'))
```

    [90m
    reason: 'To break down the project into manageable steps.'
    subtasks: ['Brainstorm ideas for book', 'Create an outline', 'Write first draft of each chapter', 'Revise and edit each chapter', 'Finalize book structure and content', 'Proofread and format for publication'][30m



```python
subtasksResp = TaskSplitterOutput.from_dataclass(resp)
```


```python
subtasksResp.reason

```




    'To break down the project into manageable steps.'




```python
subtasksResp.subtasks
```




    ['Brainstorm ideas for book',
     'Create an outline',
     'Write first draft of each chapter',
     'Revise and edit each chapter',
     'Finalize book structure and content',
     'Proofread and format for publication']




```python
print(task_splitter)
```

    TaskSplitter: (task) -> (subtasks)



```python
subtasksResp.subtasks
```




    ['Choose a genre/topic for the book',
     'Research and gather information on the topic',
     'Create an outline for the book',
     'Write the first draft',
     'Revise and edit the book',
     'Get feedback and make necessary changes',
     'Design and format the book',
     'Publish the book']




```python
run(task_splitter, TaskSplitterInput(task='Write a book'))
```


```python

```


```python
raw_req = formatter.format_prompt(prompt=prompt_creator, input_value={
   'purpose': 'Split a task into subtasks',
#     'background': '',
#     'purpose': 'Score how you can answer the question by given context with reasoning',
#     'background': 'score should be integer 0 to 100. output parameters should be "reason" and "score" keeping this order.',
})
print(raw_req)
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    Cell In[10], line 1
    ----> 1 raw_req = formatter.format_prompt(prompt=prompt_creator, input_value={
          2    'purpose': 'Split a task into subtasks',
          3 #     'background': '',
          4 #     'purpose': 'Score how you can answer the question by given context with reasoning',
          5 #     'background': 'score should be integer 0 to 100. output parameters should be "reason" and "score" keeping this order.',
          6 })
          7 print(raw_req)


    File ~/go/src/github.com/zawakin/promptgen/promptgen/prompt_formatter.py:54, in PromptFormatter.format_prompt(self, prompt, input_value)
         52             raise TypeError(f"Expected prompt to be an instance of Prompt, got {type(prompt).__name__}.")
         53         if prompt.input_parameters.keys() != input_value.keys():
    ---> 54             raise ValueError(
         55                 f"Expected input_value to have the same keys as prompt.input_parameters, got {input_value.keys()}; wanted {prompt.input_parameters.keys()}."
         56             )
         57         formatted_input = self.input_formatter.format(input_value)
         58         return f"""{self.format_prompt_without_input(prompt)}
         59 --------
         60 
         61 Input:
         62 {formatted_input}
         63 Output:"""


    ValueError: Expected input_value to have the same keys as prompt.input_parameters, got dict_keys(['purpose']); wanted dict_keys(['purpose', 'background']).



```python
raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')
```

    [90m
    prompt: {'name': 'TaskSplitter', 'description': 'Split a task into subtasks', 'input_parameters': {'task': {'description': 'The task to be split'}, 'num_subtasks': {'description': 'The number of subtasks to split the task into'}}, 'output_parameters': {'subtasks': {'description': 'The subtasks that the task was split into'}}, 'template': {'input': {'task': 'task description', 'num_subtasks': 2}, 'output': {'subtasks': ['subtask 1', 'subtask 2']}}, 'examples': []}[30m



```python
contextual_question_score = pg.load_prompt_from_dict( formatter.parse(raw_resp)['prompt'])
contextual_question_score
```


```python
key_value_formatter = pg.KeyValuePromptFormatter()
raw_req = key_value_formatter.format_prompt(contextual_question_score, {
    'question': '水とは何？',
    'context': '熱中症には、水を飲むのが大事です',
})
print(raw_req)

raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')
```


```python
task_splitter = pg.load_prompt_from_dict( formatter.parse(raw_resp)['prompt'])
task_splitter
```


```python
print(raw_req)
```


```python
raw_req = formatter.format_prompt(task_splitter, {
    'task_desciption': 'Write a "hello, world" program in Python',
    'subtask_count': 5,
})

raw_resp = get_llm_response(raw_req)
```


```python
raw_
```


```python
subtasks = formatter.parse(raw_resp)['subtasks']
```


```python
subtasks
```


```python
raw_req = formatter.format_prompt(prompt=prompt_creator, input_value={
    'purpose': 'Receive subtask and generate Python program using given context',
    'background': 'The name of the output parameter generated should be "code". Context should be dict type.',
})
raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')
subtask_runner = pg.load_prompt_from_dict( formatter.parse(raw_resp)['prompt'])
```


```python
loader('PromptExampleCreator')
```


```python
raw_req = formatter.format_prompt(prompt=loader('PromptExampleCreator'), input_value={
    'prompt': subtask_runner.model_dump(),
    'n': 3,
})
raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')
subtask_runner_examples = formatter.parse(raw_resp)['examples']
```


```python
subtask_runner = subtask_runner.with_examples(subtask_runner_examples)
```


```python
code_formatter = pg.PromptFormatter(output_formatter=pg.CodeOutputFormatter('python'))
```


```python
subtask_context = {
    'ultimate_task': 'Write a "hello, world" program in Python',
    'subtasks': [{'subtask': subtask, 'status': 'not started', 'result': ''} for subtask in subtasks],
}

for i in range(3):
    subtask = subtasks[i]
    raw_req = code_formatter.format_prompt(prompt=subtask_runner, input_value={
        'subtask': subtask,
        'context': subtask_context,
    })
    raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')

    subtask_context['subtasks'][i] = {
        'subtask': subtask,
        'status': 'done',
        'result': raw_resp,
    }
    if i+1 < len(subtasks):
        subtask_context['subtasks'][i+1]['status'] = 'in progress',
    print(raw_resp)
```


```python
subtasks
```


```python
subtask_context = {
}
```


```python
raw_req = code_formatter.format_prompt(prompt=subtask_runner, input_value={
    'subtask': subtasks['subtasks'][1],
    'context': subtask_context,
})
raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')
code_formatter.parse(raw_resp)['code']
```


```python
raw_req
```


```python
subtask_context['task_history'].append({
            'subtask': subtasks['subtasks'][1],
            'result': raw_resp,
})
```


```python
subtask_context
```


```python
raw_req = code_formatter.format_prompt(prompt=subtask_runner, input_value={
    'subtask': subtasks['subtasks'][2],
    'context': subtask_context,
})
raw_resp = get_llm_response(raw_req, model='gpt-3.5-turbo')
code_formatter.parse(raw_resp)['code']
```


```python
print(raw_req)
```
