# 「コード生成プロンプト」を自動生成してみよう

`PromptCreator` は、プロンプトを生成するプロンプトです。

この例では、 `PromptCreator` を使って、「Pythonコードジェネレータ」プロンプトを作成します。

```python
import promptgen as pg
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


```python
formatter = pg.KeyValuePromptFormatter()
```

## 大規模言語モデルの準備

今回は、OpenAI ChatCompletion API `gpt-3.5-turbo` を使います。


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

## プロンプトを生成する


```python
# define PromptCreatorInput and PromptCreatorOutput
class PromptCreatorInput(pg.InputValue):
    purpose: str
    background: str

class PromptCreatorOutput(pg.OutputValue):
    prompt: pg.Prompt

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

作成したプロンプトを使って、Pythonコードを生成してみましょう。

タスクは、標準入力をストリームとして読み取り、標準出力に大文字の文字列を書き込む Python コードを生成することです。

```python
raw_req = formatter.format_prompt(code_generator, pg.InputValue.from_dict({
    'task': 'read stdin as stream and write stdout the upper-case string'
}))
raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo')

print(raw_resp)
```

## 生の出力

    reason: """The task requires converting all characters in a string to upper-case and then reading from stdin and writing to stdout"""
    code: """import sys
    for line in sys.stdin:
        sys.stdout.write(line.upper())"""


## パースされた出力

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


実際に `uppsercase_converter.py` として保存して実行してみましょう。

```console
$ python ./docs_src/examples/uppercase_converter.py
asdf
ASDF
hoge
HOGE
aaaaaaaaaaaaa
AAAAAAAAAAAAA
```

## まとめ

`PromptCreator` を使って、プロンプトを自動生成する例を紹介しました。
コードを生成するプロンプトを作成し、実際にコードを生成してみました。
