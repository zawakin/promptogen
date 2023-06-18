# %% [markdown]
# # プロンプトを自動生成してみよう
#
# `PromptCreator` は、目的と背景を入力として、プロンプトを自動生成するプロンプトです。
#
# PromptGenでは、プロンプトのモデルそのものも入出力パラメータとして扱うことができます。これにより、プロンプトを自動生成するプロンプトを作成することができます。

# %%
from typing import List
from pydantic import BaseModel
import promptgen as pg
from promptgen.dataclass import DataClass

# %%
collection = pg.PromptCollection(load_predefined=True)
print(collection)

# %% [markdown]
# ## プロンプトを生成するプロンプト
#
# `PromptCreator` は、プロンプトを生成するプロンプトです。
#
# 入力パラメータは、以下の通りです。
#
# ```python
# class PromptCreatorInput(InputValue):
#     purpose: str
#     background: str
# ```
#
# 出力パラメータは、以下の通りです。
#
# ```python
# class PromptCreatorOutput(OutputValue):
#     prompt: Prompt
# ```

# %%
prompt_creator = collection['PromptCreator']
prompt_creator

# %% [markdown]
# プロンプトを文字列にフォーマットすると、以下のようになります。

# %%
formatter = pg.KeyValuePromptFormatter()

print(formatter.format_prompt_without_input(prompt=prompt_creator))

#%%

from promptgen import Prompt, InputValue, OutputValue, Example, ParameterInfo

p = Prompt(
    name='function calling creator',
    description='Create a function calling code from given task',
    input_parameters=[
        ParameterInfo(name='task', description='The task for which function calling code needs to be generated'),
    ],
    output_parameters=[
        ParameterInfo(name='function', description='Function calling code generated to complete the tas'),
    ],
    template=Example(
        input=InputValue.from_dict({
            'task': 'task name',
        }),
        output=OutputValue.from_dict({
            'function': {
                "name": "function name",
                "description": "function description",
                "parameters": {
                    "type": "type of parameters",
                    "properties": {
                        "parameter 1": {
                            "type": "type of parameter 1",
                            "description": "description of parameter 1"
                        },
                        "parameter 2": {
                            "type": "type of parameter 2",
                            "enum": ["enum 1", "enum 2"]
                        }
                    },
                    "required": ["parameter 1"]
                }
            }
        })
    ),
    examples=[
        Example(
            input=InputValue.from_dict({
                'task': 'Get current weather',
            }),
            output=OutputValue.from_dict({
                'function': {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                        },
                        "required": ["location"]
                    }
                }
            })
        ),
    ],
)

# %% [markdown]
# ## 大規模言語モデルの準備
#
# 今回は、 `gpt-3.5-turbo` を使います。

# %%
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
    if not isinstance(resp, dict):
        raise Exception(resp)
    return resp['choices'][0]['message'].get('content', '')

# %%


class PromptCreatorInput(pg.InputValue):
    purpose: str
    background: str


class PromptCreatorOutput(pg.OutputValue):
    prompt: pg.Prompt

#%%


#%%

class ExampleCreatorInput(pg.InputValue):
    prompt: pg.Prompt


class ExampleCreatorOutput(pg.OutputValue):
    example: pg.Example


example_creator = collection['PromptExampleCreator']

# %%
raw_req = formatter.format_prompt(example_creator, input_value=ExampleCreatorInput(
    prompt=p,
))
raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo')
resp = ExampleCreatorOutput.from_dataclass(formatter.parse(example_creator, raw_resp))

#%%

code_generator = pg.Prompt.from_dict(resp.prompt)
code_generator

# %% [markdown]
# 作成したプロンプトを使って、タスクを分解してみましょう。

# %%
raw_req = formatter.format_prompt(code_generator, pg.InputValue.from_dict({
    'task': 'read stdin as stream and write stdout the upper-case string'
}))
raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo')

print(raw_resp)

# %%
output_value = formatter.parse(code_generator, raw_resp)
output_value

# %%
print(output_value['code'])



# %%
