# フォーマッター


## JsonPromptFormatter

フォーマッターをカスタマイズすることで、出力を変更することができます。

```python
import promptogen as pg

summarizer = pg.Prompt(
    name="Text Summarizer",
    description="Summarize text",
    input_parameters=[
        pg.ParameterInfo(name="text", description="Text to summarize"),
    ],
    output_parameters=[
        pg.ParameterInfo(name="summary", description="Summary of text"),
    ],
    template=pg.Example(
        input=pg.InputValue(text="This is a sample text to summarize."),
        output=pg.OutputValue(summary="This is a summary of the text."),
    ),
    examples=[
        pg.Example(
            input=pg.InputValue(text="One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."),
            output=pg.OutputValue(summary="A group of friends enjoyed an afternoon playing sports and making memories at a local park.")
        )
    ],
)

formatter = pg.JsonPromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
```

出力:

````console
You are an AI named "Text Summarizer".
Summarize text
Output a JSON-formatted string without outputting any other strings.
Be careful with the order of brackets in the json.

Input Parameters:
  - text: Text to summarize

Output Parameters:
  - summary: Summary of text

Template:
Input:
```json
{"text": "This is a sample text to summarize."}```
Output:
```json
{
 "summary": "This is a summary of the text."
}```

Example 1:
Input:
```json
{"text": "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."}```
Output:
```json
{
 "summary": "A group of friends enjoyed an afternoon playing sports and making memories at a local park."
}```

````


