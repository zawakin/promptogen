# プロンプトを自動生成してみよう

`PromptCreator` は、目的と背景を入力として、プロンプトを自動生成するプロンプトです。

PromptoGenでは、プロンプトのモデルそのものも入出力パラメータとして扱うことができます。これにより、プロンプトを自動生成するプロンプトを作成することができます。


```python
import promptogen as pg
```


```python
collection = pg.PromptCollection(load_predefined=True)
print(collection)
```

    <PromptCollection>
    Number of prompts: 6
    
    Prompts:
    - TextCategorizer: (text: str, categories: list) -> (category: str, found: bool)
    - TextSummarizer: (text: str) -> (summary: str)
    - PromptExampleCreator: (prompt: Prompt, n: int) -> (examples: list)
    - PromptCreator: (purpose: str, background: str) -> (prompt: Prompt)
    - PromptOptimizer: (original_prompt: Prompt, background: str) -> (optimized_prompt: Prompt)
    - PythonCodeGenerator: (task: str) -> (reason: str, code: str)
    


## プロンプトを生成するプロンプト

`PromptCreator` は、プロンプトを生成するプロンプトです。

入力パラメータは、以下の通りです。

```python
class PromptCreatorInput(InputValue):
    purpose: str
    background: str
```

出力パラメータは、以下の通りです。

```python
class PromptCreatorOutput(OutputValue):
    prompt: Prompt
```


```python
prompt_creator = collection['PromptCreator']
prompt_creator
```




    Prompt: PromptCreator
    
    Create a prompt from the given purpose. Don't create an example with the input purpose. Instead, create an example with a different purpose. Consider background information that is necessary to understand the purpose.
    
    Input Parameters:
        - purpose (str): purpose of the prompt
        - background (str): background of the prompt
    
    Output Parameters:
        - prompt (Prompt): prompt created from the given purpose. Is has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.



プロンプトを文字列にフォーマットすると、以下のようになります。


```python
formatter = pg.KeyValuePromptFormatter()

print(formatter.format_prompt_without_input(prompt=prompt_creator))
```

    You are an AI named "PromptCreator".
    Create a prompt from the given purpose. Don't create an example with the input purpose. Instead, create an example with a different purpose. Consider background information that is necessary to understand the purpose.
    You should follow 'Template' format. The format is 'key: value'.
    
    Input Parameters:
      - purpose: purpose of the prompt
      - background: background of the prompt
    
    Output Parameters:
      - prompt: prompt created from the given purpose. Is has 'name', 'description', 'input_parameters', 'output_parameters', 'template', and 'examples'.
    
    Template:
    Input:
    purpose: """purpose of the prompt"""
    background: """background of the prompt"""
    Output:
    prompt: { 'name': 'sample-new prompt',
      'description': 'A sample prompt.',
      'input_parameters': [{'name': 'input1', 'description': 'The first input parameter.'}, {'name': 'input2', 'description': 'The second input parameter.'}],
      'output_parameters': [{'name': 'output1', 'description': 'The first output parameter.'}, {'name': 'output2', 'description': 'The second output parameter.'}],
      'template': {'input': {'input1': 'Hello, world!', 'input2': 'Hello, world!'}, 'output': {'output1': 'Hello, world!', 'output2': 'Hello, world!'}},
      'examples': [ {'input': {'input1': 'Hello, world!', 'input2': 'Hello, world!'}, 'output': {'output1': 'Hello, world!', 'output2': 'Hello, world!'}},
                    {'input': {'input1': 'Hello, world!', 'input2': 'Hello, world!'}, 'output': {'output1': 'Hello, world!', 'output2': 'Hello, world!'}}]}
    
    Example 1:
    Input:
    purpose: """Categorize the given text into one of the given categories."""
    background: """The given text may be a sentence, a paragraph, or a document."""
    Output:
    prompt: { 'name': 'TextCategorizer',
      'description': 'Categorize the given text',
      'input_parameters': [ {'name': 'text', 'description': 'The text to be categorized'},
                            {'name': 'categories', 'description': 'The categories to categorize the text into'}],
      'output_parameters': [ {'name': 'category', 'description': 'The category the text belongs to'},
                             {'name': 'found', 'description': 'Whether the category was found in the text'}],
      'template': {'input': {'text': 'text', 'categories': ['category 1', 'category 2']}, 'output': {'category': 'category 1', 'found': True}},
      'examples': [ { 'input': { 'text': 'A recent study shows that regular exercise can help improve cognitive function in older adults.',
                                 'categories': ['Health', 'Science', 'Technology']},
                      'output': {'category': 'Health', 'found': True}}]}
    
    Example 2:
    Input:
    purpose: """Python code generator"""
    background: """style: input: (task: str), output: (reason: str, code: str)"""
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
    


## 大規模言語モデルの準備

今回は、 `gpt-3.5-turbo` を使います。


```python
import openai
import os

from dotenv import load_dotenv
load_dotenv('../../.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

def generate_llm_response(prompt: str, model: str) -> str:
    resp = openai.ChatCompletion.create(model=model, messages=[
        {'role': 'user', 'content': prompt}
    ], max_tokens=2048)
    return resp['choices'][0]['message'].get('content', '')
```


```python
class PromptCreatorInput(pg.InputValue):
    purpose: str
    background: str

class PromptCreatorOutput(pg.OutputValue):
    prompt: pg.Prompt
```


```python
raw_req = formatter.format_prompt(prompt_creator, PromptCreatorInput(
    purpose='Generate Python code from given task',
    background='style: input: (task: str), output: (reason: str, code: str)')
)
raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo')
resp = PromptCreatorOutput.from_dataclass(formatter.parse(prompt_creator, raw_resp))

code_generator = pg.Prompt.from_dict(resp.prompt)
code_generator
```




    Prompt: PythonCodeGenerator2
    
    Generate Python code based on the given task.
    
    Input Parameters:
        - task (str): The task for which the Python code needs to be generated
    
    Output Parameters:
        - reason (str): The reason for the generated Python code
        - code (str): The Python code generated to complete the task



作成したプロンプトを使って、タスクを分解してみましょう。


```python
raw_req = formatter.format_prompt(code_generator, pg.InputValue.from_dict({
    'task': 'read stdin as stream and write stdout the upper-case string'
}))
raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo')

print(raw_resp)
```

    reason: """The task requires converting all characters in a string to upper-case and then reading from stdin and writing to stdout"""
    code: """import sys
    for line in sys.stdin:
        sys.stdout.write(line.upper())"""



```python
output_value = formatter.parse(code_generator, raw_resp)
output_value
```




    OutputValue(reason='The task requires converting all characters in a string to upper-case and then reading from stdin and writing to stdout', code='import sys\nfor line in sys.stdin:\n    sys.stdout.write(line.upper())')




```python
print(output_value['code'])
```

    import sys
    for line in sys.stdin:
        sys.stdout.write(line.upper())

