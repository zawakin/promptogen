from typing import List
from pydantic import BaseModel
import pytest
from promptgen.dataclass import DataClass

from promptgen.input import InputValue, JsonInputFormatter, KeyValueInputFormatter


@pytest.fixture
def dataclass() -> BaseModel:
    class TmpBaseModel(BaseModel):
        test_input_parameter_name: str
        test_input_parameter_name_2: str

    return TmpBaseModel(
        test_input_parameter_name='test input parameter value',
        test_input_parameter_name_2='test input parameter value 2'
    )


def test_input_value_custom():
    class InnerInputValue(DataClass):
        value: str

    class CustomInputValue(InputValue):
        outer_value: str
        inner_value: InnerInputValue
        inner_values: List[InnerInputValue]


    d = {
        'outer_value': 'outer value',
        'inner_value': {
            'value': 'inner value'
        },
        'inner_values': [
            {
                'value': 'inner value 1'
            }
        ]
    }

    assert CustomInputValue.from_dict(d) == CustomInputValue(
        outer_value=d['outer_value'],
        inner_value=InnerInputValue(value=d['inner_value']['value']),
        inner_values=[
            InnerInputValue(value=d['inner_values'][0]['value'])
        ]
    )
    assert CustomInputValue.from_dict(d).dict() == d
    assert CustomInputValue.from_dict(d)['inner_value'] == InnerInputValue(value='inner value')
    assert CustomInputValue.from_dict(d)['inner_values'] == [InnerInputValue(value='inner value 1')]


def test_input_value_from_dict():
    assert InputValue.from_dict({
        'test_input_parameter_name': 'test input parameter value',
        'test_input_parameter_name_2': 'test input parameter value 2'
    }) == InputValue(
        test_input_parameter_name='test input parameter value',
        test_input_parameter_name_2='test input parameter value 2'
    )


def test_input_value_from_dict_invalid():
    with pytest.raises(TypeError):
        InputValue.from_dict(10)  # type: ignore


def test_input_value_from_BaseModel(dataclass: BaseModel):
    assert InputValue.from_dataclass(dataclass) == InputValue(
        test_input_parameter_name='test input parameter value',
        test_input_parameter_name_2='test input parameter value 2'
    )


def test_input_value_from_BaseModel_invalid():
    with pytest.raises(TypeError):
        InputValue.from_dataclass(10)  # type: ignore


def test_json_input_formatter_format():
    f = JsonInputFormatter()

    assert f.format(InputValue.from_dict({
        'test input parameter name': 'test input parameter value',
        'test input parameter name 2': 'test input parameter value 2'
    })) == f"""```json
{{"test input parameter name": "test input parameter value", "test input parameter name 2": "test input parameter value 2"}}```"""


def test_json_input_formatter_format_invalid():
    f = JsonInputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore


def test_key_value_input_formatter_format():
    f = KeyValueInputFormatter()

    assert f.format(InputValue.from_dict({
        'test input parameter name': 'test input parameter value',
        'test input parameter name 2': 'test input parameter value 2',
        'nested': {
            'test input parameter name': 'test input parameter value',
        },
    })) == f'''test input parameter name: """test input parameter value"""
test input parameter name 2: """test input parameter value 2"""
nested: {{'test input parameter name': 'test input parameter value'}}'''


def test_key_value_input_formatter_format_invalid():
    f = KeyValueInputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore
