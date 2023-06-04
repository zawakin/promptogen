import pytest
from promptgen.dataclass import DataClass

from promptgen.output import CodeOutputFormatter, JsonOutputFormatter, KeyValueOutputFormatter, OutputValue, TextOutputFormatter


@pytest.fixture
def dataclass():
    class Tmp(DataClass):
        test_output_parameter_name: str = 'test output parameter value' # type: ignore
        test_output_parameter_name_2: str = 'test output parameter value 2' # type: ignore

    return Tmp()


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


def test_output_value_from_dataclass(dataclass: DataClass):
    assert OutputValue.from_dataclass(dataclass) == OutputValue(
        test_output_parameter_name='test output parameter value',
        test_output_parameter_name_2='test output parameter value 2'
    )


def test_output_value_from_dataclass_invalid():
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


def test_code_output_formatter_description():
    f = CodeOutputFormatter('python')

    assert f.description() == """Output a code-block in python without outputting any other strings."""


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

    with pytest.raises(ValueError):
        f.format(OutputValue.from_dict({
            'cod': 'print("hello world")',
        }))


def test_code_output_formatter_parse():
    f = CodeOutputFormatter('python')

    assert f.parse("""```python
print("hello world")```""") == {
        'code': 'print("hello world")',
    }


def test_text_output_formatter_description():
    f = TextOutputFormatter()

    assert f.description() == ""


def test_text_output_formatter_format():
    f = TextOutputFormatter()

    assert f.format(OutputValue.from_dict({
        'text': 'hello world',
    })) == f"""hello world"""


def test_text_output_formatter_format_invalid():
    f = TextOutputFormatter()

    with pytest.raises(TypeError):
        f.format(10)  # type: ignore

    with pytest.raises(ValueError):
        f.format(OutputValue.from_dict({
            'tex': 'print("hello world")',
        }))

    with pytest.raises(TypeError):
        f.format(OutputValue.from_dict({
            'text': 10,
        }))


def test_text_output_formatter_parse():
    f = TextOutputFormatter()

    assert f.parse("""hello world""") == {
        'text': 'hello world',
    }


def test_key_value_output_formatter_description():
    f = KeyValueOutputFormatter()

    assert f.description() == """You should follow 'Template' format. The format is 'key: value'."""


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


def test_key_value_output_formatter_parse_syntax_error():
    f = KeyValueOutputFormatter()

    with pytest.raises(SyntaxError):
        f.parse("""test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2""")


def test_key_value_output_formatter_parse_invalid():
    f = KeyValueOutputFormatter()

    with pytest.raises(ValueError):
        f.parse("""test output parameter name: 'test output parameter value'
test output parameter name 2: 'test output parameter value 2'
test output parameter name 3""")


def test_key_value_output_formatter_parse_invalid_input():
    f = KeyValueOutputFormatter()

    with pytest.raises(TypeError):
        f.parse(1) # type: ignore
