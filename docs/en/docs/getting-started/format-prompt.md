## PromptFormatter

In PromptoGen, you can flexibly create formatters to turn prompts into strings.

To understand `PromptFormatter`, please refer to [Formatting Values](format-value.md) and [Parsing Values](parse-value.md).

## Formatting a prompt into a string without input parameters

The prompt named `summarizer` used on this page was created in [Prompt Examples](prompt.md).

To format a string without input parameters, use the formatter's `format_prompt_without_input` method. This method takes the prompt and the formatter as arguments and formats the prompt into a string.

### Example: KeyValuePromptFormatter

We will use the `KeyValuePromptFormatter`.
This formatter outputs the keys and values of the input/output variables in the form of `key: value`.

- Input parameters are formatted using `KeyValueFormatter`.
- Output parameters are also formatted using `KeyValueFormatter`.

```python
formatter = pg.KeyValuePromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
```

Console output:

```console
Summarize text and extract keywords.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of the text
  - keywords: Keywords extracted from the text

Template:
Input:
text: "This is a sample text to summarize."
Output:
summary: """This is a summary of the text."""
keywords: [
 "sample",
 "text",
 "summarize"
]

Example 1:
Input:
text: "One sunny afternoon, a group of friends gathered at a nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
keywords: [
 "friends",
 "park",
 "sports",
 "memories"
]
```

### Example: JsonPromptFormatter

We will use the `JsonPromptFormatter`.
This formatter outputs the keys and values of the input/output variables in JSON format.

```python
formatter = pg.JsonPromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
```

Console output:

```console
Summarize text and extract keywords.

Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of the text
  - keywords: Keywords extracted from the text

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
 "text": "One sunny afternoon, a group of friends gathered at a nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
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
```

### Example: Custom Formatter

By specifying an input formatter and output formatter to `PromptFormatter`, you can create a custom formatter. In this example, we use `KeyValueFormatter` as the input formatter and `JsonValueFormatter` as the output formatter.

```python
from promptogen.prompt_formatter import KeyValueFormatter, JsonValueFormatter

formatter = pg.PromptFormatter(
    input_formatter=KeyValueFormatter(),
    output_formatter=JsonValueFormatter(),
)
print(formatter.format_prompt_without_input(summarizer))
```

Console output:

```console
Summarize text and extract keywords.

Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of the text
  - keywords: Keywords extracted from the text

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
text: "One sunny afternoon, a group of friends gathered at a nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
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
```

## Formatting a prompt into a string with input parameters

Next, let's try formatting a prompt into a string with input parameters.

To format a prompt into a string with input parameters, use the `format_prompt` method.

Input parameters can be specified by passing a `pg.Value` (i.e., a `dict`) to the `format_prompt` method.

```python
formatter = pg.KeyValuePromptFormatter()

input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to produce and maintain well-structured, efficient code, and address challenges that emerge from implementation complexities, changing user requirements, and system optimization.",
}
print(formatter.format_prompt(summarizer, input_value))
```

Console output:

```console
Summarize text and extract keywords.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of the text
  - keywords: Keywords extracted from the text

Template:
Input:
text: "This is a sample text to summarize."
Output:
summary: """This is a summary of the text."""
keywords: [
 "sample",
 "text",
 "summarize"
]

Example 1:
Input:
text: "One sunny afternoon, a group of friends gathered at a nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
keywords: [
 "friends",
 "park",
 "sports",
 "memories"
]

--------

Input:
text: "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to produce and maintain well-structured, efficient code, and address challenges that emerge from implementation complexities, changing user requirements, and system optimization."
```

## Modifying Display Items

You can modify the display items using `pg.PromptFormatterConfig`.

```python
class PromptFormatterConfig(DataClass):
    """Configuration for formatting a prompt.

    Attributes:
        show_formatter_description (bool): Whether to display the description of the formatter.
        show_parameter_info (bool): Whether to display the parameter info of the prompt.
        show_template (bool): Whether to display the template of the prompt.
    """

    show_formatter_description: bool = True
    show_parameter_info: bool = True
    show_template: bool = True
```

For instance, if you don't want to format information like `Input Parameters` or `Output Parameters`, you specify it as follows:

```python
config = PromptFormatterConfig(
  show_parameter_info=False
)
formatter = pg.KeyValueFormatter(config)
```
