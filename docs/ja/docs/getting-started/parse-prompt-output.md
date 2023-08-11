## PromptFormatter

`PromptFormatter` は、LLMから返ってきた出力文字列から `Value` をパースするメソッドを提供します。

内部では　`ValueFormatter` を使用しているため、詳細は [Valueをパースする](parse-value.md) を参照してください。


`PromptFormatter` は `output_formatter` という `ValueFormatter` 型のパラメータを持ちます。このパラメータは、 `Value` をLLMからの出力文字列に変換したり、LLMからの出力文字列を `Value` に変換するために使用されます。

## 出力をPythonオブジェクトに変換する

出力をPythonオブジェクトに変換してみましょう。
`formatter.parse` メソッドを使用することで、LLMからの出力文字列をプロンプトの出力パラメータを用いてパースできます。パースの結果はPythonの `dict` に格納されます。

[Valueをパースする](parse-value.md) を参照してください。

このページで使用する `summarizer` という名前のプロンプトは [Promptの例](prompt.md) で作成したものです。

```python
import promptogen as pg

formatter = pg.KeyValuePromptFormatter()

raw_resp = """summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']"""
summarized_resp = formatter.parse(summarizer, raw_resp)
print(summarized_resp)
```

コンソール出力:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```
