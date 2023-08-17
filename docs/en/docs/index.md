# PromptoGen

<a href="/" target="_blank"><img src="img/logo-light-mode.svg#only-light" style="width: 90%; padding-left: 10%;"></a>
<a href="/" target="_blank"><img src="img/logo-dark-mode.svg#only-dark" style="width: 90%; padding-left: 10%;"></a>

<p style="text-align: center;">
    <em>Bridging LLMs and Python Seamlessly.</em>
</p>

----

:material-file-document-alert: Documentation: https://promptogen.zawakin.dev

:material-github: Source Code: https://github.com/zawakin/promptogen

:material-rocket: For the Quick Start Guide, click [here](getting-started/installation.md).

:material-earth: [English](/) | [日本語](/ja/)

----

## :material-book-multiple: About PromptoGen

### :material-lightbulb: PromptoGen Project Vision

**"Achieving efficient and extensible communication with Large Language Models (LLM)"**

1. **Seamless Conversion between LLM I/O and Python Objects**: Facilitate natural and efficient communication with LLMs.
2. **Unique Abstraction Interface**: Offer users high customizability and extensibility.
3. **Eliminating Dependency on LLM Communication**: Aim to build a robust system capable of flexibly adapting to future evolutions and changes in LLMs.

### :material-thought-bubble: Problems with Existing Libraries

Other libraries: Due to often managing everything from LLM communication to text generation and parsing, the following issues arise:

1. :material-thought-bubble: **Difficulty in forming a prompt-engineering ecosystem.**
2. :material-thought-bubble: **High dependence on LLM, making it vulnerable to LLM changes and evolution.**
3. :material-thought-bubble: **Complex implementation with low customizability.**

### :material-check-circle: Solutions

1. :material-check-circle: **`Prompt` Data Class**: **Fostering a prompt engineering ecosystem** 
    - Defines basic LLM communication information (name, description, input/output info, template, examples).
2. :material-check-circle: **`TextLLM` Interface**: **Ensuring independence from LLM implementations**
    - Communication with LLM is through the `TextLLM` interface.
3. :material-check-circle: **`PromptFormatter` Interface**: **Enhancing customizability**
    - Users can define any formatter.
    - Generates prompt strings from `Prompt` and input.
    - Converts LLM text output to Python data structures.


### :material-star-shooting: Benefits for Users
- :material-puzzle: **Modularity**: Freedom to combine.
- :material-plus: **Extensibility**: Ability to add custom formatters and parsers.
- :material-shield-half-full: **Independence**: Unaffected by new models or libraries.
- :material-wrench: **Maintainability**: Simplified management and troubleshooting.
- :material-clock: **Development Efficiency**: No need to change the implementation for each LLM


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
import promptogen as pg

summarizer = pg.Prompt.from_json_file("summarizer.json")
```

Here's the translated text in English:

### TextLLM: Flexible LLM Integration

Through `pg.TextLLM`, PromptoGen achieves collaboration with a variety of large-scale language models (LLM).

```python title="Implementation example of TextLLM interface"
import promptogen as pg

class YourTextLLM(pg.TextLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, text: str) -> str:
        return generate_by_your_text_llm(text, self.model)

text_llm = YourTextLLM(model="your-model")
```

By adopting this interface, PromptoGen can seamlessly incorporate different LLMs and their versions. Users can utilize various LLMs in a consistent manner regardless of the specific LLM.

### PromptRunner: Execute Prompts Efficiently

`pg.PromptRunner` supports the execution of prompts simply and efficiently.

```python hl_lines="7 18" title="Prompt execution using PromptRunner"
import promptogen as pg

# Prepare an LLM that implements the `pg.TextLLM` interface
text_llm = YourTextLLM(model="your-model")

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
```

Advantages of this tool:

1. **Abstraction**: Users can execute prompts without being aware of the specific LLM implementation.
2. **Consistency**: Changes are minimized when executing the same prompt with different LLMs.
3. **Extensibility**: Adding new prompts or modifying existing ones is easy.

`pg.PromptRunner` is a key tool for making prompt execution more intuitive and efficient using PromptoGen.

## Quick Start Guide

Please refer to the [Quick Start Guide](getting-started/quickstart.md).

## Application Examples

Refer to [Application Examples](examples/index.md).

- Auto Prompt Generation
- LLM I/O Inferences Generation
- ...

## Dependent Libraries

PromptoGen only depends on [Pydantic](https://docs.pydantic.dev/latest/) to define the data class.

## Limitations

- With updates to PromptoGen, compatibility with prompts outputted in JSON may be lost.
- The large language models tested for operation are OpenAI's `gpt-3.5-turbo`, `gpt-4`, and Meta's `Llama 2`. Other large language models have not been tested for operation. In particular, there may be cases where the parser does not work correctly, so please be cautious.

## Contribution

Bug reports, proposals for new features, pull requests, etc., are all welcome! For more details, please see [Contribution](contributing.md).

## License

MIT License
