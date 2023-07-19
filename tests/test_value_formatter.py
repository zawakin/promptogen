from typing import List, Tuple
from pydantic import BaseModel
import pytest

from promptgen import JsonValueFormatter, KeyValueFormatter


@pytest.fixture
def dataclass():
    class Tmp(BaseModel):
        test_output_parameter_name: str = 'test output parameter value' # type: ignore
        test_output_parameter_name_2: str = 'test output parameter value 2' # type: ignore

    return Tmp()


@pytest.fixture
def output_keys() -> List[Tuple[str, type]]:
    return [
        ('test output parameter name', str),
        ('test output parameter name 2', str)
    ]


def test_json_output_formatter_format():
    f = JsonValueFormatter(indent=None)

    assert f.format({
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }) == f"""```json
{{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}}```"""


def test_json_output_formater_format_invalid():
    f = JsonValueFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore


def test_json_output_formatter_parse():
    f = JsonValueFormatter()
    output_keys = [
        ('test output parameter name', str),
        ('test output parameter name 2', str)
    ]

    assert f.parse(output_keys, """```json
{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}```""") == {
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }


def test_json_output_formatter_parse_no_code_block(output_keys: List[Tuple[str, type]]):
    f = JsonValueFormatter()

    with pytest.raises(ValueError):
        f.parse(output_keys, """{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}""")


def test_json_output_formatter_parse_invalid_json(output_keys: List[Tuple[str, type]]):
    f = JsonValueFormatter()

    with pytest.raises(ValueError):
        f.parse(output_keys, """```json
{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2""")


def test_key_value_output_formatter_description():
    f = KeyValueFormatter()

    assert f.description() == ""


def test_key_value_output_formatter_format():
    f = KeyValueFormatter()

    assert f.format({
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }) == f'''test output parameter name: "test output parameter value"
test output parameter name 2: "test output parameter value 2"'''


def test_key_value_output_formatter_format_invalid():
    f = KeyValueFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore


def test_key_value_output_formatter_parse(output_keys: List[Tuple[str, type]]):
    f = KeyValueFormatter()

    assert f.parse(output_keys, """test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2'""") == {
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }

    assert f.parse([('key1', str), ('key2', str)], """key1: 'value1'
key2: 'value2'""") == {
        'key1': 'value1',
        'key2': 'value2'
    }

    assert f.parse([('key1', str), ('key2', str)], """key1: value1
key2: value2""") == {
        'key1': 'value1',
        'key2': 'value2'
    }

    assert f.parse([('key1', str)], """key1: 'value1'""") == {
        'key1': 'value1'
    }

    assert f.parse([('key1', list)], """key1: ['value1', 'value2']""") == {
        'key1': ['value1', 'value2']
    }

    # triple quote
    assert f.parse([('key1', str)], """key1: \"\"\"value1\"\"\" (this value1 is string)""") == {
        'key1': 'value1'
    }

    # double quote
    assert f.parse([('key1', str)], """key1: \"value1\" (this value1 is string)""") == {
        'key1': 'value1'
    }

    assert f.parse([('key1', str), ('key2', list)], """
                   key1: 'value1'
        key2: [
            'value2-1',
            'value2-2'
        ]
    """) == {
        'key1': 'value1',
        'key2': ['value2-1', 'value2-2']
    }


def test_key_value_output_formatter_parse_syntax_error(output_keys: List[Tuple[str, type]]):
    f = KeyValueFormatter()

    with pytest.raises(SyntaxError):
        f.parse(output_keys, """test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2""")


def test_key_value_output_formatter_parse_invalid(output_keys: List[Tuple[str, type]]):
    f = KeyValueFormatter()

    with pytest.raises(SyntaxError):
        f.parse(output_keys, """test output parameter name: 'test output parameter value'
test output parameter name 2:'""")


def test_key_value_output_formatter_parse_invalid_input():
    f = KeyValueFormatter()

    with pytest.raises(TypeError):
        f.parse(1) # type: ignore
