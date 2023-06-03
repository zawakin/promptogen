import pytest

from promptgen.output import CodeOutputFormatter, JsonOutputFormatter, KeyValueOutputFormatter, OutputValue


def test_json_output_formatter_name():
    f = JsonOutputFormatter()

    assert f.name() == "json"


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

    assert f.parse("""```json
{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}```""") == {
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }


def test_json_output_formatter_parse_no_code_block():
    f = JsonOutputFormatter()

    with pytest.raises(ValueError):
        f.parse("""{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2"}""")


def test_json_output_formatter_parse_invalid_json():
    f = JsonOutputFormatter()

    with pytest.raises(ValueError):
        f.parse("""```json
{"test output parameter name": "test output parameter value", "test output parameter name 2": "test output parameter value 2""")


def test_code_output_formatter_format():
    f = CodeOutputFormatter('python')

    assert f.format(OutputValue.from_dict({
        'code': 'print("hello world")',
    })) == f"""```python
print("hello world")```"""

def test_code_output_formatter_format_invalid():
    f = CodeOutputFormatter('python')

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore

def test_code_output_formatter_parse():
    f = CodeOutputFormatter('python')

    assert f.parse("""```python
print("hello world")```""") == {
        'code': 'print("hello world")',
    }

def test_key_value_output_formatter_format():
    f = KeyValueOutputFormatter()

    assert f.format(OutputValue.from_dict({
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    })) == f"""test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2'"""

def test_key_value_output_formatter_format_invalid():
    f = KeyValueOutputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore

def test_key_value_output_formatter_parse():
    f = KeyValueOutputFormatter()

    assert f.parse("""test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2'""") == {
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }
