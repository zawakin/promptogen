## PromptFormatter

PromptoGenでは、プロンプトを文字列にするためのフォーマッターを柔軟に作成できます。

`PromptFormatter` を理解するために、 [Valueをフォーマットする](format-value.md) と [Valueをパースする](parse-value.md) を参照してください。

## プロンプトを入力パラメータなしで文字列にフォーマットする

このページで使用する `summarizer` という名前のプロンプトは [Promptの例](prompt.md) で作成したものです。

入力パラメータなしで文字列にフォーマットするには、フォーマッターの `format_prompt_without_input` メソッドを使用します。
このメソッドは、プロンプトとフォーマッターを引数に取り、プロンプトを文字列にフォーマットします。

### 例: KeyValuePromptFormatter

`KeyValuePromptFormatter` というフォーマッターを使用します。
このフォーマッターは、入出力変数のキーとバリューを `key: value` の形式で出力します。

- 入力パラメータは `KeyValueFormatter` を使用してフォーマットされます。
- 出力パラメータは `KeyValueFormatter` を使用してフォーマットされます。

```python
formatter = pg.KeyValuePromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
```

コンソール出力:

```console
Summarize text and extract keywords.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text
  - keywords: Keywords extracted from text

Template:
Input:
text: "This is a sample text to summarize."
Output:
summary: """This is a summary of the text."""
keywords: ['sample', 'text', 'summarize']

Example 1:
Input:
text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
keywords: ['friends', 'park', 'sports', 'memories']
```

### 例: JsonPromptFormatter

`JsonPromptFormatter` というフォーマッターを使用します。
このフォーマッターは、入出力変数のキーとバリューをJSON形式で出力します。

````console
Summarize text and extract keywords.

Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text
  - keywords: Keywords extracted from text

Template:
Input:
```json
{
 "text": "This is a sample text to summarize."
}```
Output:
```json
{
 "summary": "This is a summary of the text.",
 "keywords": [
  "sample",
  "text",
  "summarize"
 ]
}```

Example 1:
Input:
```json
{
 "text": "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
}```
Output:
```json
{
 "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
 "keywords": [
  "friends",
  "park",
  "sports",
  "memories"
 ]
}```
````

### 例: カスタムフォーマッター

`PromptFormatter` に入力フォーマッターと出力フォーマッターを指定することで、カスタムフォーマッターを作成できます。
この例では、`KeyValueFormatter` を入力フォーマッターとして、`JsonValueFormatter` を出力フォーマッターとして使用します。

```python
from promptogen.prompt_formatter import KeyValueFormatter, JsonValueFormatter

formatter = pg.PromptFormatter(
    input_formatter=KeyValueFormatter(),
    output_formatter=JsonValueFormatter(),
)
print(formatter.format_prompt_without_input(summarizer))
```

コンソール出力:

````console
Summarize text and extract keywords.

Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text
  - keywords: Keywords extracted from text

Template:
Input:
text: "This is a sample text to summarize."
Output:
```json
{
 "summary": "This is a summary of the text.",
 "keywords": [
  "sample",
  "text",
  "summarize"
 ]
}```

Example 1:
Input:
text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
```json
{
 "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
 "keywords": [
  "friends",
  "park",
  "sports",
  "memories"
 ]
}```
````

## プロンプトを入力パラメータありで文字列にフォーマットする

続いて、プロンプトを入力パラメータありで文字列にフォーマットしてみましょう。

プロンプトを入力パラメータ込みで文字列にフォーマットするには、`format_prompt` メソッドを使用します。

入力パラメータは、 `pg.Value` つまり  `dict` を `format_prompt` メソッドに渡すことで指定できます。

```python
formatter = pg.KeyValuePromptFormatter()

input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.",
}
print(formatter.format_prompt(summarizer, input_value))
```

コンソール出力:

```console
Summarize text and extract keywords.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text
  - keywords: Keywords extracted from text

Template:
Input:
text: "This is a sample text to summarize."
Output:
summary: """This is a summary of the text."""
keywords: ['sample', 'text', 'summarize']

Example 1:
Input:
text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
keywords: ['friends', 'park', 'sports', 'memories']

--------

Input:
text: "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization."
Output:
```


```console
summary: """Software developers collaborate using version control systems like Git to create and maintain efficient code and solve implementation and optimization issues."""
keywords: ['software engineering', 'developers', 'collaborate', 'projects', 'version control systems', 'Git', 'code', 'implementation complexities', 'evolving user requirements', 'system optimization']
```

## 出力をPythonオブジェクトに変換する

続いて、出力をPythonオブジェクトに変換してみましょう。
`formatter.parse` メソッドを使用することで、LLMからの出力文字列をプロンプトの出力パラメータを用いてパースできます。パースの結果はPythonの `dict` に格納されます。

[Valueをパースする](parse-value.md) を参照してください。

```python
summarized_resp = formatter.parse(summarizer, raw_resp)
print(summarized_resp)
```

コンソール出力:

```console
{'summary': 'Software developers collaborate using version control systems like Git to create and maintain efficient code and solve implementation and optimization issues.', 'keywords': ['software engineering', 'developers', 'collaborate', 'projects', 'version control systems', 'Git', 'code', 'implementation complexities', 'evolving user requirements', 'system optimization']}
```
