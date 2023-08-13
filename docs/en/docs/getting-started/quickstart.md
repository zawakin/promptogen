## Import
    
```python
import promptogen as pg
```

## Create a Simple Prompt

First, let's create a simple prompt. In this quickstart guide, we'll create a prompt that takes a text as input and outputs its summary and keywords.

In other words, we will create a prompt that realizes the function `(text: str) -> (summary: str, keywords: List[str])`.

PromptoGen provides a data class (`pg.Prompt`) to represent prompts.
Using this data class, we'll create the prompt.
This data class inherits from `pydantic.BaseModel`.

To create a prompt, the following information is needed:

| Item                       | Argument Name                | Type                                      |
|----------------------------|-----------------------------|------------------------------------------|
| Prompt Name                | `name`                      | `str`                                    |
| Prompt Description         | `description`               | `str`                                    |
| List of Input Parameters   | `input_parameters`          | `List[pg.ParameterInfo]`                 |
| List of Output Parameters  | `output_parameters`         | `List[pg.ParameterInfo]`                 |
| I/O Template               | `template`                  | `pg.IOExample`                           |
| List of I/O Examples       | `examples`                  | `List[pg.IOExample]`                     |

Using this information, let's create a prompt.

```python
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
    template=pg.IOExample(
        input={'text': "This is a sample text to summarize."},
        output={
            'summary': "This is a summary of the text.",
            'keywords': ["sample", "text", "summarize"],
        },
    ),
    examples=[
        pg.IOExample(
            input={
                'text': "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."},
            output={
                'summary': "A group of friends enjoyed an afternoon playing sports and making memories at a local park.",
                'keywords': ["friends", "park", "sports", "memories"],
            },
        )
    ],
)
```

## Format the Prompt to String without Input Parameters

First, let's format the prompt to a string without input parameters.

In PromptoGen, you can flexibly create formatters to turn prompts into strings.

Here, we use a formatter named `KeyValuePromptFormatter` which outputs the input-output variables in the form `key: value`.

To format the prompt to a string without input parameters, use the `format_prompt_without_input` method.
This method takes the prompt and formatter as arguments and formats the prompt into a string.

```python
formatter = pg.KeyValuePromptFormatter()
print(formatter.format_prompt_without_input(summarizer))
```

Console Output:

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
keywords: [
 "sample",
 "text",
 "summarize"
]

Example 1:
Input:
text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: """A group of friends enjoyed an afternoon playing sports and making memories at a local park."""
keywords: [
 "friends",
 "park",
 "sports",
 "memories"
]
```

## Format the Prompt to String with Input Parameters

Next, let's format the prompt to a string with input parameters.

Input parameters are specified using a `dict`.

To format the prompt to a string with input parameters, use the `format_prompt` method.

```python
input_value = {
    'text': "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization.",
}
print(formatter.format_prompt(summarizer, input_value))
```

Console Output:

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
keywords: [
 "sample",
 "text",
 "summarize"
]

Input:
text: "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization."
Output:
```

## Generating Output Using Large Language Models

Next, let's try generating output from a large language model.

This library does not provide functionality to generate output from large language models, but it can be achieved using the OpenAI ChatGPT API.

Here, using the OpenAI ChatGPT API, let's generate a summarized text from the input text.

In advance, set the OpenAI API Key and Organization ID as environment variables.

```python
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

def generate_chat_completion(text: str, model: str) -> str:
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        max_tokens=2048,
        stream=True,
    )
    raw_resp = ""
    for chunk in resp:
        chunk_content = chunk["choices"][0]["delta"].get("content", "")
        raw_resp += chunk_content

    return raw_resp

# Create TextLLM
text_llm = pg.FunctionBasedTextLLM(
    generate_text_by_text=lambda input_text: generate_chat_completion(input_text, "gpt-3.5-turbo"),
)
```

`TextLLM` is an abstract class in PromptoGen to uniformly handle large language models. `pg.FunctionBasedTextLLM` is an implementation of `TextLLM` that generates output from large language models using a function.

Next, let's format the prompt with input parameters into a string and generate output from the large language model.

```python
# Use the formatter to format the prompt into a string with input parameters
raw_req = formatter.format_prompt(summarizer, input_value)

# Generate output from the large language model
raw_resp = text_llm.generate(raw_req)

print(raw_resp)
```

Console Output:

```console
summary: """Software engineers collaborate using Git to create and maintain efficient code, and address implementation issues and user requirements."""
keywords: [
 "software engineering",
 "developers",
 "collaborate",
 "projects",
 "version control systems",
 "Git",
 "code",
 "implementation complexities",
 "user requirements",
 "system optimization"
]
```

## Convert the Output to a Python Object

Next, since the LLM output is just a string, let's convert it to a Python object. By using the `formatter.parse` method, you can parse the output string from the LLM using the output parameters of the prompt. The parsing result is stored in a Python `dict`.

```python
summarized_resp = formatter.parse(summarizer, raw_resp)
print(summarized_resp)
```

Console Output:

```console
{'summary': 'Software engineers collaborate using Git to create and maintain efficient code, and address implementation issues and user requirements.', 'keywords': ['software engineering', 'developers', 'collaborate', 'projects', 'version control systems', 'Git', 'code', 'implementation complexities', 'user requirements', 'system optimization']}
```

This output is a `dict` that is the result of parsing the LLM output string.

## Conclusion

We've introduced the basic usage of PromptoGen.

The flow introduced here is as follows:

1. Define the prompt
2. Define the formatter
3. Use the formatter to format the prompt and input parameters into a string
4. Generate output using the large language model
5. Convert the output to a Python object

Although the example introduced here is simple, with PromptoGen, you can easily handle more complex prompts and input/output parameters.

Furthermore, you can specify the prompt itself as input or output parameters, making it possible to dynamically generate prompts.
