import pytest
from promptogen.model.prompt import IOExample, ParameterInfo, Prompt

from promptogen import JsonPromptFormatter, KeyValuePromptFormatter, PromptFormatter, PromptFormatterInterface
from promptogen.model.value_formatter import ValueFormatter
from promptogen.prompt_formatter import JsonValueFormatter, KeyValueFormatter


@pytest.fixture
def json_prompt_formatter() -> PromptFormatterInterface:
    input_formatter: ValueFormatter = JsonValueFormatter(indent=None)
    output_formatter: ValueFormatter = JsonValueFormatter(indent=None)
    return PromptFormatter(input_formatter=input_formatter, output_formatter=output_formatter)


@pytest.fixture
def prompt():
    return Prompt(
        name='test name',
        description='test description',
        input_parameters=[
            ParameterInfo(name="test input parameter name", description='test input parameter description'),
            ParameterInfo(name="test input parameter name 2", description='test input parameter description 2'),
        ],
        output_parameters=[
            ParameterInfo(name="test output parameter name", description='test output parameter description'),
            ParameterInfo(name="test output parameter name 2", description='test output parameter description 2'),
        ],
        template=IOExample(
            input={
                'test input parameter name': 'test input parameter value',
                'test input parameter name 2': 'test input parameter value 2'
            },
            output={
                'test output parameter name': 'test output parameter value',
                'test output parameter name 2': 'test output parameter value 2'
            },
        ),
        examples=[
            IOExample(
                input={
                    'test input parameter name': 'example test input parameter value',
                    'test input parameter name 2': 'example test input parameter value 2'
                },
                output={
                    'test output parameter name': 'example test output parameter value',
                    'test output parameter name 2': 'example test output parameter value 2'
                },
            ),
            IOExample(
                input={
                    'test input parameter name': 'example test input parameter value 3',
                    'test input parameter name 2': 'example test input parameter value 4'
                },
                output={
                    'test output parameter name': 'example test output parameter value 3',
                    'test output parameter name 2': 'example test output parameter value 4'
                },
            ),
        ])


def test_prompt_formatter_format_prompt(json_prompt_formatter: PromptFormatterInterface, prompt: Prompt):
    input_value = {
        'test input parameter name': 'sample value',
        'test input parameter name 2': 'sample value 2'
    }
    assert json_prompt_formatter.format_prompt(prompt=prompt, input_value=input_value) == f"""test description

Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - test input parameter name: test input parameter description
  - test input parameter name 2: test input parameter description 2

Output Parameters:
  - test output parameter name: test output parameter description
  - test output parameter name 2: test output parameter description 2

Template:
Input:
```json
{{"test input parameter name": "test input parameter value", "test input parameter name 2": "test input parameter value 2"}}```
Output:
```json
{{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}}```

Example 1:
Input:
```json
{{"test input parameter name": "example test input parameter value", "test input parameter name 2": "example test input parameter value 2"}}```
Output:
```json
{{"test output parameter name": "example test output parameter value", "test output parameter name 2": "example test output parameter value 2"}}```

Example 2:
Input:
```json
{{"test input parameter name": "example test input parameter value 3", "test input parameter name 2": "example test input parameter value 4"}}```
Output:
```json
{{"test output parameter name": "example test output parameter value 3", "test output parameter name 2": "example test output parameter value 4"}}```

--------

Input:
```json
{{"test input parameter name": "sample value", "test input parameter name 2": "sample value 2"}}```
Output:"""


def test_prompt_formatter_format_prompt_invalid(json_prompt_formatter: PromptFormatterInterface, prompt: Prompt):
    input_value = {
        'test input parameter name': 'sample value',
        'test input parameter name 2': 'sample value 2'
    }
    with pytest.raises(TypeError):
        json_prompt_formatter.format_prompt(prompt=prompt, input_value=10) # type: ignore

    with pytest.raises(TypeError):
        json_prompt_formatter.format_prompt(prompt=object(), input_value=input_value) # type: ignore

    with pytest.raises(ValueError):
        json_prompt_formatter.format_prompt(prompt=prompt, input_value={})


def test_prompt_formatter_format_prompt_without_input(json_prompt_formatter: PromptFormatterInterface, prompt: Prompt):
    assert json_prompt_formatter.format_prompt_without_input(prompt) == f"""test description

Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - test input parameter name: test input parameter description
  - test input parameter name 2: test input parameter description 2

Output Parameters:
  - test output parameter name: test output parameter description
  - test output parameter name 2: test output parameter description 2

Template:
Input:
```json
{{"test input parameter name": "test input parameter value", "test input parameter name 2": "test input parameter value 2"}}```
Output:
```json
{{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}}```

Example 1:
Input:
```json
{{"test input parameter name": "example test input parameter value", "test input parameter name 2": "example test input parameter value 2"}}```
Output:
```json
{{"test output parameter name": "example test output parameter value", "test output parameter name 2": "example test output parameter value 2"}}```

Example 2:
Input:
```json
{{"test input parameter name": "example test input parameter value 3", "test input parameter name 2": "example test input parameter value 4"}}```
Output:
```json
{{"test output parameter name": "example test output parameter value 3", "test output parameter name 2": "example test output parameter value 4"}}```
"""


def test_prompt_formatter_parse(json_prompt_formatter: PromptFormatterInterface, prompt: Prompt):
    output_value = {
        'test output parameter name': 'sample value',
        'test output parameter name 2': 'sample value 2'
    }
    assert json_prompt_formatter.parse(prompt, """```json
{"test output parameter name": "sample value", "test output parameter name 2": "sample value 2"}```""") == output_value


def test_json_prompt_formatter():
    f: PromptFormatterInterface = JsonPromptFormatter()

    assert type(f.input_formatter) == JsonValueFormatter
    assert type(f.output_formatter) == JsonValueFormatter


def test_key_value_prompt_formatter():
    f: PromptFormatterInterface = KeyValuePromptFormatter()

    assert type(f.input_formatter) == KeyValueFormatter
    assert type(f.output_formatter) == KeyValueFormatter
