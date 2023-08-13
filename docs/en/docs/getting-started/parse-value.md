Similarly to formatting, you can use `ValueFormatter` to parse a string into a `Value`.

### Example: `KeyValueFormatter`

```python
from promptogen.prompt_formatter import KeyValueFormatter

s = """summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']"""

value_formatter = KeyValueFormatter()
parsed_value = value_formatter.parse([
    ("summary", str),
    ("keywords", list),
], s)
print(parsed_value)
```

Output:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```

`parsed_value` will be a `dict`.

### Example: `JsonValueFormatter`

```python
from promptogen.prompt_formatter import JsonValueFormatter

s = """```json
{
 "summary": "This is a summary of the text.",
 "keywords": [
  "sample",
  "text",
  "summarize"
 ]
}```"""

parsed_value = value_formatter.parse([
    ("summary", str),
    ("keywords", list),
], value_formatter.format(value))
print(parsed_value)
```

Output:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```

`parsed_value` will be a `dict`.
