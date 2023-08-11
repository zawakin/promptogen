フォーマットと同様に `ValueFormatter` を使用して、文字列から`Value`をパースすることができます。


### 例: `KeyValueFormatter`

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

出力:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```

### 例: `JsonValueFormatter`

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

出力:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```
