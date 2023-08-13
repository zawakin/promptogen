`ValueFormatter` is a class used to convert a `Value` into a string and to parse the output.

### Example: `KeyValueFormatter`

`KeyValueFormatter` converts a `Value` into a list of key-value pairs.

```python
from promptogen.prompt_formatter import KeyValueFormatter

value_formatter = KeyValueFormatter()

value = {
    'summary': "This is a summary of the text.",
    'keywords': ["sample", "text", "summarize"],
}
print(value_formatter.format(value))
```

Output:

```console
summary: "This is a summary of the text."
keywords: [
 "sample",
 "text",
 "summarize"
]
```

### Example: `JsonValueFormatter`

Using `json.dumps`, `JsonValueFormatter` converts a `Value` into a formatted JSON string.

```python
from promptogen.prompt_formatter import JsonValueFormatter

value_formatter = JsonValueFormatter()

value = {
    'summary': "This is a summary of the text.",
    'keywords': ["sample", "text", "summarize"],
}
print(value_formatter.format(value))
```

Output:

````console
```json
{
 "summary": "This is a summary of the text.",
 "keywords": [
  "sample",
  "text",
  "summarize"
 ]
}
```
````

## In More Detail

`ValueFormatter` is an abstract class, and both `KeyValueFormatter` and `JsonValueFormatter` inherit from `ValueFormatter`.

```python
# from promptogen.model.value_formatter import ValueFormatter

class ValueFormatter(ABC):
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def format(self, value: Value) -> str:
        pass

    @abstractmethod
    def parse(self, key_types: List[Tuple[str, type]], s: str) -> Value:
        pass
```

## In Conclusion

Usually, you won't use `ValueFormatter` directly but will utilize `PromptFormatter`. However, for the sake of understanding the concept, we explained how to format prompts using `ValueFormatter`.
