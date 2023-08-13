This page describes how to create a prompt that splits a task into smaller subtasks.

## Source Code

[task-splitter.py (GitHub)](https://github.com/zawakin/promptogen/tree/main/examples/promptcreation/task_splitter.py)

## Setup

`openai_util.OpenAITextLLM` is the `TextLLM` defined on the [OpenAITextLLM page](openai-text-llm.md) (see also: [TextLLM](../getting-started/text-llm.md)). If you define them in the same directory's `openai_util.py`, you can `import` them.

```python
import promptogen as pg
from openai_util import OpenAITextLLM
from promptogen.prompt_collection import PromptCreatorPrompt

llm = OpenAITextLLM(model="gpt-3.5-turbo")

formatter = pg.KeyValuePromptFormatter()
prompt_runner = pg.TextLLMPromptRunner(llm=llm, formatter=formatter)

prompt_creator_prompt = PromptCreatorPrompt()
```

## Creating the Prompt

```python
def setup_task_splitter_prompt() -> pg.Prompt:
    input_value = {
        "description": "Split a task into subtasks.",
        "background": "(task: str) -> (strategy: str, subtasks: List[str])",
    }
    resp = prompt_runner.run_prompt(prompt_creator_prompt, input_value=input_value)
    return pg.Prompt.from_dict(resp["prompt"])


task_splitter_prompt = setup_task_splitter_prompt()
print(task_splitter_prompt)
# TaskSplitter: (task: str) -> (strategy: str, subtasks: list)

# Description
# -----------
# Split a task into subtasks.

# Input Parameters
# ----------------
# - task (str): The task to be split into subtasks

# Output Parameters
# -----------------
# - strategy (str): The strategy used to split the task
# - subtasks (list): The list of subtasks generated from the task

# Examples Count
# --------------
# 1
```

## Running the Prompt

```python

input_value = {
    "task": "Make a system that can remind me to go running every day.",
}

output_value = prompt_runner.run_prompt(task_splitter_prompt, input_value=input_value)

print(output_value["strategy"])
# "Break down the task into smaller steps related to developing the reminder system"

print(output_value["subtasks"])
# ['Design a user interface for the reminder system', "Create a database to store the user's running schedule", 'Develop a notification system to send reminders to the user', "Implement a feature to track and record the user's running progress", 'Test and debug the reminder system for any issues', 'Deploy the reminder system on a suitable platform']
```
