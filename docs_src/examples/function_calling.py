# %%
import promptgen as pg
from promptgen import Prompt, InputValue, OutputValue, Example, ParameterInfo

# %%
collection = pg.PromptCollection(load_predefined=True)
formatter = pg.KeyValuePromptFormatter()

function_calling_prompt = Prompt(
    name='function calling creator',
    description='Create a function calling code from given task',
    input_parameters=[
        ParameterInfo(name='task', description='The task for which function calling code needs to be generated'),
    ],
    output_parameters=[
        ParameterInfo(name='function', description='Function calling code generated to complete the task'),
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

#%%
import openai
import os

from dotenv import load_dotenv
load_dotenv()

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


class ExampleCreatorInput(pg.InputValue):
    prompt: pg.Prompt


class ExampleCreatorOutput(pg.OutputValue):
    example: pg.Example


example_creator = collection['PromptExampleCreator']

# %%
raw_req = formatter.format_prompt(example_creator, input_value=ExampleCreatorInput(
    prompt=function_calling_prompt,
))
raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo')
resp = ExampleCreatorOutput.from_dataclass(formatter.parse(example_creator, raw_resp))

print(resp)
