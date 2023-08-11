`ValueFormatter`は、`Value`の値を文字列に変換し、出力をパースするためのクラスです。

### 例: `KeyValueFormatter`

`KeyValueFormatter` は、`Value`をキーと値のペアのリストに変換します。

```python
from promptogen.prompt_formatter import KeyValueFormatter

value_formatter = KeyValueFormatter()

value = {
    'summary': "This is a summary of the text.",
    'keywords': ["sample", "text", "summarize"],
}
print(value_formatter.format(value))
```

出力:

```console
summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']
```

### 例: `JsonValueFormatter`

`json.dumps` を使用した `JsonValueFormatter` は、`Value`を整形されたJSON文字列に変換します。

```python
from promptogen.prompt_formatter import JsonValueFormatter

value_formatter = JsonValueFormatter()

value = {
    'summary': "This is a summary of the text.",
    'keywords': ["sample", "text", "summarize"],
}
print(value_formatter.format(value))
```

出力:

````console
```json
{
 "summary": "This is a summary of the text.",
 "keywords": [
  "sample",
  "text",
  "summarize"
 ]
}```
````

## さらに詳しく

`ValueFormatter` は抽象クラスであり、`KeyValueFormatter`と`JsonValueFormatter`は、`ValueFormatter`を継承しています。

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


## さいごに

普段は、`ValueFormatter`を直接使用することはなく、 `PromptFormatter`を使用します。
しかし、概念を理解するために、`ValueFormatter`を使用してプロンプトをフォーマットする方法を説明しました。
