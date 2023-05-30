import pytest
from promptgen.input import JsonInputFormatter
from promptgen.output import JsonOutputFormatter
from promptgen.prompt import Example, ParameterInfo, Prompt

from promptgen.prompt_formatter import PromptFormatter, PromptFormatterInterface


@pytest.fixture
def prompt_formatter():
    input_formatter = JsonInputFormatter()
    output_formatter = JsonOutputFormatter(indent=None)
    return PromptFormatter(input_formatter=input_formatter, output_formatter=output_formatter)


@pytest.fixture
def prompt():
    return Prompt(
        name='test name',
        description='test description',
        input_parameters={
            "test input parameter name": ParameterInfo(
                description='test input parameter description',
            ),
            "test input parameter name 2": ParameterInfo(
                description='test input parameter description 2',
            ),
            },
        output_parameters={
            "test output parameter name": ParameterInfo(
                description='test output parameter description',
            ),
            "test output parameter name 2": ParameterInfo(
                description='test output parameter description 2',
            ),
            },
        template=Example(
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
            Example(
                input={
                    'test input parameter name': 'example test input parameter value',
                    'test input parameter name 2': 'example test input parameter value 2'
                },
                output={
                    'test output parameter name': 'example test output parameter value',
                    'test output parameter name 2': 'example test output parameter value 2'
                },
            ),
            Example(
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


def test_base_prompt_formatter_format_prompt(prompt_formatter: PromptFormatterInterface, prompt: Prompt):
    input_value = {
        'test input parameter name': 'sample value',
        'test input parameter name 2': 'sample value 2'
    }
    assert prompt_formatter.format_prompt(prompt=prompt, input_value=input_value) == f"""You are an AI named \"test name\".
test description
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


def test_base_prompt_formatter_format_prompt_without_input(prompt_formatter: PromptFormatterInterface, prompt: Prompt):
    assert prompt_formatter.format_prompt_without_input(prompt) == f"""You are an AI named \"test name\".
test description
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
