#%%jj
import promptgen as pg

summarizer = pg.Prompt(
    name="Text Summarizer and Keyword Extractor",
    description="Summarize text and extract keywords.",
    input_parameters=[
        pg.ParameterInfo(name="text", description="Text to summarize"),
    ],
    output_parameters=[
        pg.ParameterInfo(name="summary", description="Summary of text"),
        pg.ParameterInfo(name="keywords", description="Keywords extracted from text"),
    ],
    template=pg.Example(
        input=pg.InputValue(text="This is a sample text to summarize."),
        output=pg.OutputValue(
            summary="This is a summary of the text.",
            keywords=["sample", "text", "summarize"],
        ),
    ),
    examples=[
        pg.Example(
            input=pg.InputValue(text="One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."),
            output=pg.OutputValue(
                summary="A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
                keywords=["friends", "park", "sports", "memories"],
            )
        )
    ],
)

formatter = pg.KeyValuePromptFormatter()


# formatter = pg.JsonPromptFormatter()

print(formatter.format_prompt_without_input(summarizer))
# %%

input_value = pg.InputValue(text="In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.")
print(formatter.format_prompt(summarizer, input_value))

# %%


import openai
import os

from dotenv import load_dotenv
load_dotenv('../experimental/.env')

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")


def generate_chat_stream_response(prompt: str, model: str):
        resp = openai.ChatCompletion.create(model=model, messages=[
            {'role': 'user', 'content': prompt}
        ], stream=True, max_tokens=2048)
        for chunk in resp:
            yield chunk['choices'][0]['delta'].get('content', '') # type: ignore


def generate_llm_response(prompt: str, model: str):
    s = ''
    for delta in generate_chat_stream_response(prompt, model):
        # print(delta, end='')
        s += delta
    return s


raw_req = formatter.format_prompt(summarizer, input_value)
raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo')

print(raw_resp)

# %%
summarized_resp = formatter.parse(raw_resp)
print(f'summary:\n{summarized_resp["summary"]}')
print('keywords:')
for keyword in summarized_resp["keywords"]:
    print(f'  - {keyword}')
