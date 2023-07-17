import json
import tempfile
from pydantic import ValidationError
import pytest

from promptgen.model.prompt import Example, ParameterInfo, Prompt, load_prompt_from_json_string


@pytest.fixture
def prompt_dict() -> dict:
    return {
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
        input_parameters=[
            ParameterInfo(
                name="test input parameter name",
                description='test input parameter description',
            ),
            ParameterInfo(
                name="test input parameter name 2",
                description='test input parameter description 2',
            ),
            ],
        output_parameters=[
            ParameterInfo(
                name="test output parameter name",
                description='test output parameter description',
            ),
            ParameterInfo(
                name="test output parameter name 2",
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
    with pytest.raises(ValidationError):
        Prompt.from_dict({})

    with pytest.raises(TypeError):
        Prompt.from_dict(None) # type: ignore


def test_prompt_to_dict(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    assert prompt.model_dump() == prompt_dict


def test_prompt_from_dict_parameter_mismatch(prompt_dict: dict):
    prompt_dict['template']['input']['test input parameter name 3'] = 'test input parameter value 3'

    with pytest.raises(ValidationError):
        Prompt.from_dict(prompt_dict)


def test_prompt_from_dict_parameter_mismatch_2(prompt_dict: dict):
    prompt_dict['input_parameters'].append({
        "name": "test input parameter name 3",
        "description": "test input parameter description 3"
    })

    with pytest.raises(ValidationError):
        Prompt.from_dict(prompt_dict)


def test_prompt_from_json_string(prompt_dict: dict):
    prompt_json = json.dumps(prompt_dict)

    prompt = Prompt.from_json_string(prompt_json)

    assert prompt.model_dump() == prompt_dict


def test_prompt_to_json_file(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    with tempfile.NamedTemporaryFile() as f:
        prompt.to_json_file(f.name)

        with open(f.name, 'r') as f2:
            assert prompt.model_dump() == json.load(f2)


def test_prompt_with_examples(prompt_dict: dict, other_example_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    got = prompt.update(examples=[Example.from_dict(other_example_dict)])

    assert type(got.examples) == list
    assert type(got.examples[0]) == Example
    assert got.examples[0].input == other_example_dict['input']
    assert got.examples[0].output == other_example_dict['output']


def test_prompt_rename_input_parameter(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    got = prompt.rename_input_parameter('test input parameter name', 'test input parameter name 3')

    assert type(got.input_parameters) == list
    assert 'test input parameter name' != got.input_parameters[0].name
    assert 'test input parameter name 3' == got.input_parameters[0].name
    assert got.input_parameters[0].description == 'test input parameter description'


def test_prompt_rename_input_parameter_invalid(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    with pytest.raises(ValueError):
        prompt.rename_input_parameter('test input parameter name 3', 'test input parameter name 3')


def test_prompt_rename_output_parameter(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    got = prompt.rename_output_parameter('test output parameter name', 'test output parameter name 3')

    assert type(got.output_parameters) == list
    assert 'test output parameter name' != got.output_parameters[0].name
    assert 'test output parameter name 3' == got.output_parameters[0].name
    assert got.output_parameters[0].description == 'test output parameter description'


def test_prompt_validate_template_valid():
    Prompt.model_validate({
    'name': 'test name',
    'description': 'test description',
    'input_parameters': [
        ParameterInfo(name='test input parameter name', description='test input parameter description')
    ],
    'output_parameters': [
        ParameterInfo(name='test output parameter name', description='test output parameter description')
    ],
    'template': Example(
        input={
            'test input parameter name': 'example test input parameter value',
        },
        output={
            'test output parameter name': 'example test output parameter value',
        },
    ),
    'examples': [
        Example(
            input={
                'test input parameter name': 'example test input parameter value',
            },
            output={
                'test output parameter name': 'example test output parameter value',
            },
        ),
    ],
})


def test_prompt_validate_template_invalid():
    # no template
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'input_parameters': [],
            'output_parameters': [],
            'examples': [],
        })

    # no examples
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'input_parameters': [],
            'output_parameters': [],
            'template': {},
        })

    # no input parameters
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'output_parameters': [],
            'template': {},
            'examples': [],
        })

    # no output parameters
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'input_parameters': [],
            'template': {},
            'examples': [],
        })

    # invalid template input
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'input_parameters': [
                ParameterInfo(name='test input parameter name', description='test input parameter description')
            ],
            'output_parameters': [
                ParameterInfo(name='test output parameter name', description='test output parameter description')
            ],
            'template': Example(
                # missing input parameter
                input={},
                output={
                    'test output parameter name': 'example test output parameter value',
                },
            ),
            'examples': [],
        })

    # invalid template output
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'input_parameters': [
                ParameterInfo(name='test input parameter name', description='test input parameter description')
            ],
            'output_parameters': [
                ParameterInfo(name='test output parameter name', description='test output parameter description')
            ],
            'template': Example(
                input={
                    'test input parameter name': 'example test input parameter value',
                },
                # missing output parameter
                output={},
            ),
            'examples': [],
        })

    # invalid example input
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'input_parameters': [
                ParameterInfo(name='test input parameter name', description='test input parameter description')
            ],
            'output_parameters': [
                ParameterInfo(name='test output parameter name', description='test output parameter description')
            ],
            'template': Example(
                input={
                    'test input parameter name': 'example test input parameter value',
                },
                output={
                    'test output parameter name': 'example test output parameter value',
                },
            ),
            'examples': [
                Example(
                    # missing input parameter
                    input={},
                    output={
                        'test output parameter name': 'example test output parameter value',
                    },
                ),
            ],
        })

    # invalid example output
    with pytest.raises(ValueError):
        Prompt.from_dict({
            'name': 'test name',
            'description': 'test description',
            'input_parameters': [
                ParameterInfo(name='test input parameter name', description='test input parameter description')
            ],
            'output_parameters': [
                ParameterInfo(name='test output parameter name', description='test output parameter description')
            ],
            'template': Example(
                input={
                    'test input parameter name': 'example test input parameter value',
                },
                output={
                    'test output parameter name': 'example test output parameter value',
                },
            ),
            'examples': [
                Example(
                    input={
                        'test input parameter name': 'example test input parameter value',
                    },
                    # missing output parameter
                    output={},
                ),
            ],
        })


def test_prompt_str(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    assert str(prompt) == """test name: (test input parameter name: str, test input parameter name 2: str) -> (test output parameter name: str, test output parameter name 2: str)"""


def test_prompt_repr(prompt_dict: dict):
    want = json.dumps(prompt_dict, indent=4, ensure_ascii=False)
    prompt = Prompt.from_dict(prompt_dict)

    assert repr(prompt) == """Prompt: test name

test description

Input Parameters:
    - test input parameter name (str): test input parameter description
    - test input parameter name 2 (str): test input parameter description 2

Output Parameters:
    - test output parameter name (str): test output parameter description
    - test output parameter name 2 (str): test output parameter description 2
"""


def test_prompt_rename_output_parameter_invalid(prompt_dict: dict):
    prompt = Prompt.from_dict(prompt_dict)

    with pytest.raises(ValueError):
        prompt.rename_output_parameter('test output parameter name 3', 'test output parameter name 3')


def test_load_prompt_from_json_string(prompt_dict: dict):
    prompt_json = json.dumps(prompt_dict)

    prompt = load_prompt_from_json_string(prompt_json)

    assert prompt.model_dump() == prompt_dict
    assert type(prompt) == Prompt
