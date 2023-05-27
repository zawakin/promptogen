import pytest

from promptogen.prompt import Example, ParameterInfo, Prompt


def test_prompt_from_dict():
    prompt = Prompt.from_dict({
        'name': 'test name',
        'description': 'test description',
        'input_parameters': [
            {
                'name': 'test input parameter name',
                'description': 'test input parameter description',
            },
            {
                'name': 'test input parameter name 2',
                'description': 'test input parameter description 2',
            }
        ],
        'output_parameters': [
            {
                'name': 'test output parameter name',
                'description': 'test output parameter description',
            },
            {
                'name': 'test output parameter name 2',
                'description': 'test output parameter description 2',
            }
        ],
        'template': {
            'input': {
                'test input parameter name': 'test input parameter value',
                'test input parameter name 2': 'test input parameter value 2'
            },
            'output': {
                'test output parameter name': 'test output parameter value',
                'test output parameter name 2': 'test output parameter value 2'
            },
        },
        'examples': [
            {
                'input': {
                    'test input parameter name': 'example test input parameter value',
                    'test input parameter name 2': 'example test input parameter value 2'
                },
                'output': {
                    'test output parameter name': 'example test output parameter value',
                    'test output parameter name 2': 'example test output parameter value 2'
                },
            },
            {
                'input': {
                    'test input parameter name': 'example test input parameter value 3',
                    'test input parameter name 2': 'example test input parameter value 4'
                },
                'output': {
                    'test output parameter name': 'example test output parameter value 3',
                    'test output parameter name 2': 'example test output parameter value 4'
                },
            }
        ]
    })

    want = Prompt(
        name='test name',
        description='test description',
        input_parameters=[
            ParameterInfo(
                name='test input parameter name',
                description='test input parameter description',
            ),
            ParameterInfo(
                name='test input parameter name 2',
                description='test input parameter description 2',
            ),
        ],
        output_parameters=[
            ParameterInfo(
                name='test output parameter name',
                description='test output parameter description',
            ),
            ParameterInfo(
                name='test output parameter name 2',
                description='test output parameter description 2',
            ),
        ],
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

    # BaseModel implements __eq__ by comparing the dict representation of the object
    assert prompt == want


def test_prompt_from_dict_invalid():
    with pytest.raises(ValueError):
        Prompt.from_dict({})
