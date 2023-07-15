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


def test_json_input_formatter_format():
    f = JsonInputFormatter()

    assert f.format({
        'test input parameter name': 'test input parameter value',
        'test input parameter name 2': 'test input parameter value 2'
    }) == f"""```json
{{"test input parameter name": "test input parameter value", "test input parameter name 2": "test input parameter value 2"}}```"""


def test_json_input_formatter_format_invalid():
    f = JsonInputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore


def test_key_value_input_formatter_format():
    f = KeyValueInputFormatter()

    assert f.format({
        'test input parameter name': 'test input parameter value',
        'test input parameter name 2': 'test input parameter value 2',
        'nested': {
            'test input parameter name': 'test input parameter value',
        },
    }) == f'''test input parameter name: """test input parameter value"""
test input parameter name 2: """test input parameter value 2"""
nested: {{'test input parameter name': 'test input parameter value'}}'''


def test_key_value_input_formatter_format_invalid():
    f = KeyValueInputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore
