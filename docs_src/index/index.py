import promptogen as pg


summarizer = pg.Prompt(
    name="Text Summarizer",
    description="Summarize text.",
    input_parameters=[
        pg.ParameterInfo(name="text", description="Text to summarize"),
    ],
    output_parameters=[
        pg.ParameterInfo(name="summary", description="Summary of text"),
    ],
    template=pg.IOExample(
        input={
            "text": "This is a sample text to summarize.",
        },
        output={
            "summary": "This is a summary of the text.",
        }
    ),
    examples=[
        # few-shots examples
    ],
)

print(summarizer)

formatter = pg.KeyValuePromptFormatter()
input_value = {
    "text": "In the realm of software engineering, ...",
}
print(formatter.format_prompt(summarizer, input_value))

# if the LLM returns the following response
raw_resp = """summary: 'Software developers collaborate on projects ...'"""

summarized_resp = formatter.parse(summarizer, raw_resp)
print('summary:')
print(f'{summarized_resp["summary"]}')
