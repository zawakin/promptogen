# PromptoGen

<a href="/" target="_blank"><img src="img/logo-light-mode.svg#only-light" style="width: 90%; padding-left: 10%;"></a>
<a href="/" target="_blank"><img src="img/logo-dark-mode.svg#only-dark" style="width: 90%; padding-left: 10%;"></a>

----

:material-file-document-alert: Documentation: https://promptogen.zawakin.dev/

:material-github: Source Code: https://github.com/zawakin/promptogen

:material-rocket: For the Quick Start Guide, click [here](getting-started/installation.md).

:material-earth: [English](/) | [日本語](/ja/)

----

## :material-book-multiple: About PromptoGen

### :material-lightbulb: Project Vision

PromptoGen facilitates the conversion between text outputs of large language models and Python objects. This allows developers to concentrate on prompt generation and analysis without the need to directly interact with these expansive language models.

### :material-thought-bubble: Problem Being Solved

A multitude of libraries exist that handle everything from interfacing with vast language models to text generation and interpretation. However, these all-in-one solutions can hinder the ability to customize specific functionalities.

### :material-check-circle: Solution

PromptoGen serves as a linguistic translation tool to simplify interactions with LLMs (Large Language Models). It offers unique features such as:

1. **Use of the `Prompt` Data Class**:
  
    - This data class has been structured to outline the fundamental details and format for liaising with an LLM.
    - Each `Prompt` encompasses the name of the prompt, a description, details on input & output parameters, and specific examples of its application.

2. **Generation of Prompt Strings and Decoding Outputs using `PromptFormatter`**:
    
    - The `PromptFormatter` accepts a `Prompt` alongside an input value, transforming them into a string prompt that the LLM can interpret.
    - It also modifies the textual response from the LLM into a Python data format (primarily dictionaries) based on the specifics of the associated `Prompt`.

### :material-star-shooting: Benefits to Users

1. **Modularity**: The liberty to integrate with other models or software.
2. **Extensibility**: The capability to incorporate custom formatters and interpreters.
3. **Independence**: Stability regardless of alterations in emerging language models or libraries.
4. **Maintainability**: Hassle-free management and troubleshooting.
5. **Development Efficiency**: Enables focus on creation without fretting about liaising with expansive language models.

## :material-laptop: Operating Environment

Python 3.8 or higher

## Installation

```sh
pip install promptogen
```

## Importing
```python
import promptogen as pg
```

## How to Use

### Creating your Prompt

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

### Format your Prompt as a String

To send an instance of the `Prompt` class to the LLM (Large Language Model) in actual use, you need to convert it into a string. With PromptoGen, you can use `pg.PromptFormatter` to convert the prompt into a string in any desired format.

#### Basic Structure of Prompt Format

The basic structure of the prompt format is as follows:

=== "Description"

    ```console title="Prompt Description" hl_lines="1"
    --8<-- "index/format_template.txt:key_value_format_template"
    ```

=== "Input Parameters"

    ```console title="Input Parameters" hl_lines="3-6"
    --8<-- "index/format_template.txt:key_value_format_template"
    ```

=== "Output Parameters"

    ```console title="Output Parameters" hl_lines="8-11"
    --8<-- "index/format_template.txt:key_value_format_template"
    ```

=== "Template"

    ```console title="Template" hl_lines="13-21"
    --8<-- "index/format_template.txt:key_value_format_template"
    ```

=== "Few-shot Examples"

    ```console title="Few-shot Examples" hl_lines="23-33"
    --8<-- "index/format_template.txt:key_value_format_template"
    ```

=== "Input Value"

    ```console title="Input Value" hl_lines="37-40"
    --8<-- "index/format_template.txt:key_value_format_template"
    ```

#### Various Formatting Styles

PromptoGen supports various formatting styles:

- KeyValue Format: `key: value`
- JSON Format: `{"key": "value"}`
- etc.


To use the `key: value` format for the prompt, use the `pg.KeyValuePromptFormatter`.
 Whether to display parameter information or templates can be set with `PromptFormatterConfig`.

By using the `formatter.format_prompt` method, you can convert the prompt and its corresponding input into a string.

=== "KeyValue Format for Prompt"

    ```python hl_lines="8 13"
    import promptogen as pg

    summarizer = pg.Prompt(
        name="Text Summarizer and Keyword Extractor",
        # ...
    )

    formatter = pg.KeyValuePromptFormatter()

    input_value = {
        "text": "In the realm of software engineering, ...",
    }
    print(formatter.format_prompt(summarizer, input_value))
    ```

=== "JSON Format for Prompt"

    ```python hl_lines="8 13"
    import promptogen as pg

    summarizer = pg.Prompt(
        name="Text Summarizer and Keyword Extractor",
        # ...
    )

    formatter = pg.JsonPromptFormatter()

    input_value = {
        "text": "In the realm of software engineering, ...",
    }
    print(formatter.format_prompt(summarizer, input_value))
    ```

<!-- <> -->

=== "KeyValue Format for Prompt"

    ```console title="Console Output" hl_lines="12 14-15 19 21-22 27"
    --8<-- "index/format_template.txt:key_value_format_summarizer"
    ```

=== "JSON Format for Prompt"

    ````console title="Console Output" hl_lines="3-4 15-18 20-28 32-35 37-46 51-54"
    --8<-- "index/format_template.txt:json_format_summarizer"
    ````

### Parsing Outputs from Large Language Models

After receiving the prompt string as input, you obtain an output from a large language model (like GPT-3.5, GPT-4).

=== "KeyValue Format for Prompt"
    ```console title="LLM Output"
    summary: "This is a summary of the text."
    keywords: ['sample', 'text', 'summarize']
    ```

=== "JSON Format for Prompt"

    ````console title="LLM Output"
    ```json
    {
        "summary": "This is a summary of the text.",
        "keywords": ["sample", "text", "summarize"]
    }
    ```
    ````

You can parse this output as:

=== "KeyValue Format for Prompt"

    ```python hl_lines="3 7"
    import promptogen as pg

    formatter = pg.KeyValuePromptFormatter()

    raw_resp = """summary: "This is a summary of the text."
    keywords: ['sample', 'text', 'summarize']"""
    summarized_resp = formatter.parse(summarizer, raw_resp)
    print(summarized_resp)
    ```

    ```console title="Console Output"
    {'summary': 'This is a summary of the text.', 'keywords': ['sample', 'text', 'summarize']}
    ```


=== "JSON Format for Prompt"

    ```python hl_lines="3 11"
    import promptogen as pg

    formatter = pg.JsonPromptFormatter()

    raw_resp = """```json
    {
        "summary": "This is a summary of the text.",
        "keywords": ["sample", "text", "summarize"]
    }
    ```"""
    summarized_resp = formatter.parse(summarizer, raw_resp)
    print(summarized_resp)
    ```

    ```console title="Console Output"
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

Please refer to the [Quick Start Guide](getting-started/quickstart.md).

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
