import pytest

from promptgen.output import JsonOutputFormatter, RawStringOutputFormatter


def test_json_output_formatter_name():
    f = JsonOutputFormatter()

    assert f.name() == "json"


def test_json_output_formatter_format():
    f = JsonOutputFormatter()

    assert f.format({
        'test output parameter name': 'test output parameter value',
        'test output parameter name 2': 'test output parameter value 2'
    }) == f"""```json
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


def test_raw_string_output_formatter_name():
    f = RawStringOutputFormatter()

    assert f.name() == "raw-string"


def test_raw_string_output_formatter_format():
    f = RawStringOutputFormatter()

    assert f.format("test output") == "test output"


def test_raw_string_output_formatter_parse():
    f = RawStringOutputFormatter()

    assert f.parse("test output") == "test output"
