`PromptFormatter` provides methods to parse a `Value` from the output string returned by the LLM.

Internally, it uses the `ValueFormatter`, so for more details, refer to [Parsing the Value](parse-value.md).

`PromptFormatter` has a parameter named `output_formatter` of type `ValueFormatter`. This parameter is used to convert a `Value` to the output string from LLM and vice versa.

## Converting Output to a Python Object

Let's try converting the output to a Python object. Using the `formatter.parse` method, you can parse the output string from the LLM using the output parameters of the prompt. The result of the parsing is stored in a Python `dict`.

The prompt named `summarizer` used on this page was created in [Prompt Example](prompt.md) and has two output parameters, `summary` and `keywords`.

If `summary` or `keywords` are not found during parsing, a `ValueError` occurs, and if there is an invalid syntax, a `SyntaxError` will be raised.

```python
import promptogen as pg

formatter = pg.KeyValuePromptFormatter()

raw_resp = """summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']"""
summarized_resp = formatter.parse(summarizer, raw_resp)
print(summarized_resp)
```

Console Output:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```
