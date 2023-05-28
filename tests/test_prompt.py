from pydantic import ValidationError
import pytest

from promptgen.prompt import Example, ParameterInfo, Prompt


@pytest.fixture
def prompt_dict() -> dict:
    return {
        'name': 'test name',
        'description': 'test description',
        'input_parameters': {
            'test input parameter name': {
                'description': 'test input parameter description',
            },
            'test input parameter name 2': {
                'description': 'test input parameter description 2',
            }
        },
        'output_parameters': {
            'test output parameter name': {
                'description': 'test output parameter description',
            },
            'test output parameter name 2': {
                'description': 'test output parameter description 2',
            }
        },
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
    }

@pytest.fixture
def other_example_dict() -> dict:
    return {
        'input': {
            'test input parameter name': 'other example test input parameter value',
            'test input parameter name 2': 'other example test input parameter value 2'
        },
        'output': {
            'test output parameter name': 'other example test output parameter value',
            'test output parameter name 2': 'other example test output parameter value 2'
        },
    }



def test_prompt_from_dict(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    want = Prompt(
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

    # BaseModel implements __eq__ by comparing the dict representation of the object
    assert prompt == want


def test_prompt_from_dict_invalid():
    with pytest.raises(ValidationError):
        Prompt.from_dict({})


def test_prompt_to_dict(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    assert prompt.dict() == prompt_dict


def test_prompt_from_dict_parameter_mismatch(prompt_dict: dict):
    prompt_dict['template']['input']['test input parameter name 3'] = 'test input parameter value 3'

    with pytest.raises(ValidationError):
        Prompt.from_dict(prompt_dict)


def test_prompt_from_dict_parameter_mismatch_2(prompt_dict: dict):
    prompt_dict['input_parameters']['test input parameter name 3'] = {
        "description": "test input parameter description 3"
    }

    with pytest.raises(ValidationError):
        Prompt.from_dict(prompt_dict)

def test_prompt_with_examples(prompt_dict: dict, other_example_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    got = prompt.with_examples([other_example_dict])

    assert type(got.examples) == list
    assert type(got.examples[0]) == Example
    assert got.examples[0].input == other_example_dict['input']
    assert got.examples[0].output == other_example_dict['output']

def test_prompt_rename_input_parameter(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    got = prompt.rename_input_parameter('test input parameter name', 'test input parameter name 3')

    assert type(got.input_parameters) == dict
    assert 'test input parameter name' not in got.input_parameters
    assert 'test input parameter name 3' in got.input_parameters
    assert got.input_parameters['test input parameter name 3'].description == 'test input parameter description'

def test_prompt_rename_output_parameter(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    got = prompt.rename_output_parameter('test output parameter name', 'test output parameter name 3')

    assert type(got.output_parameters) == dict
    assert 'test output parameter name' not in got.output_parameters
    assert 'test output parameter name 3' in got.output_parameters
    assert got.output_parameters['test output parameter name 3'].description == 'test output parameter description'
