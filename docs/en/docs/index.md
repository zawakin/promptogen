# PromptoGen

<a href="/" target="_blank"><img src="/img/logo-bg-white.svg" style="width: 90%; padding-left: 10%;"></a>

----

Documentation: https://promptogen.zawakin.dev/

Source Code: https://github.com/zawakin/promptogen

For the Quick Start Guide, click [here](getting-started/quickstart.md).

----

## 📘 About PromptoGen

### 💡 Project Vision

PromptoGen facilitates the conversion between text outputs of large language models and Python objects. This allows developers to concentrate on prompt generation and analysis without the need to directly interact with these expansive language models.

### ❌ Problem Being Solved

A multitude of libraries exist that handle everything from interfacing with vast language models to text generation and interpretation. However, these all-in-one solutions can hinder the ability to customize specific functionalities.

### ✅ Solution

PromptoGen serves as a linguistic translation tool to simplify interactions with LLMs (Large Language Models). It offers unique features such as:

1. **Use of the `Prompt` Data Class**:
  
    - This data class has been structured to outline the fundamental details and format for liaising with an LLM.
    - Each `Prompt` encompasses the name of the prompt, a description, details on input & output parameters, and specific examples of its application.

2. **Generation of Prompt Strings and Decoding Outputs using `PromptFormatter`**:
    
    - The `PromptFormatter` accepts a `Prompt` alongside an input value, transforming them into a string prompt that the LLM can interpret.
    - It also modifies the textual response from the LLM into a Python data format (primarily dictionaries) based on the specifics of the associated `Prompt`.

### 🌟 Benefits to Users

1. **Modularity**: The liberty to integrate with other models or software.
2. **Extensibility**: The capability to incorporate custom formatters and interpreters.
3. **Independence**: Stability regardless of alterations in emerging language models or libraries.
4. **Maintainability**: Hassle-free management and troubleshooting.
5. **Development Efficiency**: Enables focus on creation without fretting about liaising with expansive language models.

## Installation
```console
$ pip install promptogen
```

## Importing
```python
import promptogen as pg
```

## How to Use

### Creating Prompts

```python
import promptogen as pg

summarizer = pg.Prompt(
    name="Text Summarizer and Keyword Extractor",
    description="Summarize text and extract keywords.",
    input_parameters=[
        pg.ParameterInfo(name="text", description="Text to be summarized"),
    ],
    output_parameters=[
        pg.ParameterInfo(name="summary", description="Summarized text"),
        pg.ParameterInfo(name="keywords", description="Extracted keywords from the text"),
    ],
    template=pg.IOExample(
        input={'text': "This is a sample text for summarization."},
        output={
            'summary': "This is a summary of the text.",
            'keywords': ["sample", "text", "summarization"],
        },
    ),
    examples=[
        pg.IOExample(
            input={
                'text': "One sunny afternoon, a group of friends opted to meet at the nearby park to indulge in various sports and activities. They engaged in soccer, badminton, and basketball, reveling in the joy of camaraderie and crafting unforgettable moments together."},
            output={
                'summary': "A bunch of friends relished an afternoon of sports and bonding at a neighborhood park.",
                'keywords': ["friends", "park", "sports", "moments"],
            },
        )
    ],
)
```

### Prompt Format

To send an instance of the `Prompt` class to the LLM (Large Language Model) in actual use, you need to convert it into a string. With PromptoGen, you can use `pg.PromptFormatter` to convert the prompt into a string in any desired format.

PromptoGen supports various formatting styles:

- `key: value` format
- JSON format
- etc.

### Basic Structure of KeyValue Format

The KeyValue prompt format has the following basic structure. Whether to display parameter information or templates can be set with `PromptFormatterConfig`.

```
<Prompt Description>

Input Parameters:
  - <Description of Input Parameter 1>
  - <Description of Input Parameter 2>
  - ...

Output Parameters:
    - <Description of Output Parameter 1>
    - <Description of Output Parameter 2>
    - ...

Template:
Input:
<Name of Input Parameter 1>: <Example of Input Parameter 1>
<Name of Input Parameter 2>: <Example of Input Parameter 2>
...
Output:
<Name of Output Parameter 1>: <Example of Output Parameter 1>
<Name of Output Parameter 2>: <Example of Output Parameter 2>
...

Example 1:
Input:
<Name of Input Parameter 1>: <Value of Input Parameter 1>
<Name of Input Parameter 2>: <Value of Input Parameter 2>
...
Output:
<Name of Output Parameter 1>: <Value of Output Parameter 1>
<Name of Output Parameter 2>: <Value of Output Parameter 2>
...

...
```

To use the `key: value` format for the prompt, use the `pg.KeyValuePromptFormatter`.

By using the `formatter.format_prompt` method, you can convert the prompt and its corresponding input into a string.

```python
formatter = pg.KeyValuePromptFormatter()

input_value = {
    "text": "In the realm of software engineering, ...",
}
print(formatter.format_prompt(summarizer, input_value))
```

Console output:

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
summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']

Example 1:
Input:
text: "One sunny afternoon, a group of friends decided to gather at the nearby park to engage in various games and activities. They played soccer, badminton, and basketball, laughing and enjoying each other's company while creating unforgettable memories together."
Output:
summary: "A group of friends enjoyed an afternoon playing sports and making memories at a local park."
keywords: ['friends', 'park', 'sports', 'memories']

--------

Input:
text: "In the realm of software engineering, ..."
Output:
```

### JSON Format for Prompt

Using `pg.JsonPromptFormatter`, you can convert the prompt and its input into a JSON-formatted string.

```python
formatter = pg.JsonPromptFormatter()

input_value = {
    "text": "In the realm of software engineering, ...",
}
print(formatter.format_prompt(summarizer, input_value))
```

Console output:

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

--------

Input:
```json
{
 "text": "In the realm of software engineering, developers often collaborate on projects using version control systems like Git. They work together to create and maintain well-structured, efficient code, and tackle issues that arise from implementation complexities, evolving user requirements, and system optimization."
}```
Output:
````

### Parsing Outputs from Large Language Models

After receiving the prompt string as input, you obtain an output from a large language model (like GPT-3.5, GPT-4).

```console
summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']
```

You can parse this output as:

```python
formatter = pg.KeyValuePromptFormatter()

raw_resp = """summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']"""
summarized_resp = formatter.parse(summarizer, raw_resp)
print(summarized_resp)
```

Console output:

```console
{'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
```

### Saving the Prompt

```python
summarizer.to_json_file("summarizer.json")
```

### Loading the Prompt

```python
summarizer = pg.Prompt.from_json_file("summarizer.json")
```


## Quick Start Guide

Please refer to the [Quick Start Guide](quickstart.md).

## Application Examples

Refer to [Application Examples](examples/index.md).

## Dependent Libraries

- [Pydantic](https://docs.pydantic.dev/latest/) ... Used for defining data classes

## Limitations

- With updates to PromptoGen, compatibility with prompts outputted in JSON may be lost.
- The large language models tested for operation are OpenAI's `gpt-3.5-turbo`, `gpt-4`, and Meta's `Llama 2`. Other large language models have not been tested for operation. In particular, there may be cases where the parser does not work correctly, so please be cautious.

## Contribution

Bug reports, proposals for new features, pull requests, etc., are all welcome! For more details, please see [Contribution](contributing.md).

## License

MIT License
