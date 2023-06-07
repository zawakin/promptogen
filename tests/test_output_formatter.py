from typing import List
from pydantic import BaseModel
import pytest

from promptgen.output import JsonOutputFormatter, KeyValueOutputFormatter, OutputValue


@pytest.fixture
def dataclass():
    class Tmp(BaseModel):
        test_output_parameter_name: str = 'test output parameter value' # type: ignore
        test_output_parameter_name_2: str = 'test output parameter value 2' # type: ignore

    return Tmp()


@pytest.fixture
def output_keys() -> List[str]:
    return [
        'test output parameter name',
        'test output parameter name 2'
    ]


def test_output_value_from_dict():
    assert OutputValue.from_dict({
        'test_output_parameter_name': 'test output parameter value',
        'test_output_parameter_name_2': 'test output parameter value 2'
    }) == OutputValue(
        test_output_parameter_name='test output parameter value',
        test_output_parameter_name_2='test output parameter value 2'
    )


def test_output_value_from_dict_invalid():
    with pytest.raises(TypeError):
        OutputValue.from_dict(10)  # type: ignore


def test_output_value_from_BaseModel(dataclass: BaseModel):
    assert OutputValue.from_dataclass(dataclass) == OutputValue(
        test_output_parameter_name='test output parameter value',
        test_output_parameter_name_2='test output parameter value 2'
    )


def test_output_value_from_BaseModel_invalid():
    with pytest.raises(TypeError):
        OutputValue.from_dataclass(10)  # type: ignore


def test_json_output_formatter_format():
    f = JsonOutputFormatter(indent=None)

    assert f.format(OutputValue.from_dict({
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    })) == f"""```json
{{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}}```"""


def test_json_output_formater_format_invalid():
    f = JsonOutputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore


def test_json_output_formatter_parse():
    f = JsonOutputFormatter()
    output_keys = [
        'test output parameter name',
        'test output parameter name 2'
    ]

    assert f.parse(output_keys, """```json
{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}```""") == {
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }


def test_json_output_formatter_parse_no_code_block(output_keys: List[str]):
    f = JsonOutputFormatter()

    with pytest.raises(ValueError):
        f.parse(output_keys, """{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}""")


def test_json_output_formatter_parse_invalid_json(output_keys: List[str]):
    f = JsonOutputFormatter()

    with pytest.raises(ValueError):
        f.parse(output_keys, """```json
{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2""")


def test_key_value_output_formatter_description():
    f = KeyValueOutputFormatter()

    assert f.description() == """You should follow 'Template' format. The format is 'key: value'."""


def test_key_value_output_formatter_format():
    f = KeyValueOutputFormatter()

    assert f.format(OutputValue.from_dict({
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    })) == f'''test output parameter name: """test output parameter value"""
test output parameter name 2: """test output parameter value 2"""'''


def test_key_value_output_formatter_format_invalid():
    f = KeyValueOutputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore


def test_key_value_output_formatter_parse(output_keys: List[str]):
    f = KeyValueOutputFormatter()

    assert f.parse(output_keys, """test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2'""") == {
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }

    assert f.parse(['key1', 'key2'], """key1: 'value1'
key2: 'value2'""") == {
        'key1': 'value1',
        'key2': 'value2'
    }

    assert f.parse(['key1'], """key1: 'value1'""") == {
        'key1': 'value1'
    }

    assert f.parse(['key1'], """key1: ['value1', 'value2']""") == {
        'key1': ['value1', 'value2']
    }

    assert f.parse(['key1', 'key2'], """
                   key1: 'value1'
        key2: [
            'value2-1',
            'value2-2'
        ]
    """) == {
        'key1': 'value1',
        'key2': ['value2-1', 'value2-2']
    }


def test_key_value_output_formatter_parse_syntax_error(output_keys: List[str]):
    f = KeyValueOutputFormatter()

    with pytest.raises(SyntaxError):
        f.parse(output_keys, """test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2""")


def test_key_value_output_formatter_parse_invalid(output_keys: List[str]):
    f = KeyValueOutputFormatter()

    with pytest.raises(SyntaxError):
        f.parse(output_keys, """test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2'
test output parameter name 3""")


def test_key_value_output_formatter_parse_invalid_input():
    f = KeyValueOutputFormatter()

    with pytest.raises(TypeError):
        f.parse(1) # type: ignore
