import pytest

from promptgen.input import CodeInputFormatter, InputValue, JsonInputFormatter, KeyValueInputFormatter


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


def test_json_input_formatter_name():
    f = JsonInputFormatter()

    assert f.name() == "json"


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


def test_code_input_formatter_format():
    f = CodeInputFormatter('python')

    assert f.format(InputValue.from_dict({
        'code': 'print("hello world")',
    })) == f"""```python
print("hello world")```"""


def test_code_input_formatter_format_invalid():
    f = CodeInputFormatter('python')

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore


def test_key_value_input_formatter_format():
    f = KeyValueInputFormatter()

    assert f.format(InputValue.from_dict({
        'test input parameter name': 'test input parameter value',
        'test input parameter name 2': 'test input parameter value 2'
    })) == f"""test input parameter name: 'test input parameter value'
test input parameter name 2: 'test input parameter value 2'"""
