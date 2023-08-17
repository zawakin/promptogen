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


# --8<-- [start:your-text-llm]
class YourTextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_by_your_text_llm(text, self.model)


text_llm = YourTextLLM(model="your-model")
# --8<-- [end:your-text-llm]

# --8<-- [start:prompt-runner]
formatter = pg.KeyValuePromptFormatter()
runner = pg.TextLLMPromptRunner(llm=text_llm, formatter=formatter)

summarizer = pg.Prompt(
    name="Text Summarizer and Keyword Extractor",
    # ...
)

input_value = {
    "text": "In the realm of software engineering, ...",
}
output_value = runner.run_prompt(summarizer, input_value)
print(output_value)
# --8<-- [end:prompt-runner]
