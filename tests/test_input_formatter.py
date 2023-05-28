import pytest

from promptgen.input import CodeInputFormatter, JsonInputFormatter


def test_json_input_formatter_name():
    f = JsonInputFormatter()

    assert f.name() == "json"


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

def test_code_input_formatter_format():
    f = CodeInputFormatter('python')

    assert f.format({
        'code': 'print("hello world")',
    }) == f"""```python
print("hello world")```"""

def test_code_input_formatter_format_invalid():
    f = CodeInputFormatter('python')

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore

