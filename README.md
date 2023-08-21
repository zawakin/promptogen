# PromptoGen

<a href="/" target="_blank"><img src="docs/en/docs/img/logo-light-mode.svg#only-light"></a>

<p style="text-align: center;">
    <em>Bridging LLMs and Python Seamlessly.</em>
</p>

----

**Documentation**: https://promptogen.zawakin.dev

**Source** Code: https://github.com/zawakin/promptogen

**Getting Started**: https://promptogen.zawakin.dev/getting-started/installation


- [en - English](https://promptogen.zawakin.dev)
- [ja - 日本語](https://promptogen.zawakin.dev/ja)

----

## Project Vision of PromptoGen

**"Achieving efficient and expandable communication with Large Language Models (LLM)"**

1. **Seamless Conversion between LLM I/O and Python Objects**: Facilitate natural and efficient communication with LLMs.
2. **Unique Abstraction Interface**: Offer users high customizability and extensibility.
3. **Eliminating Dependency on LLM Communication**: Aim to build a robust system capable of flexibly adapting to future evolutions and changes in LLMs.

## Problems with Existing Libraries

Many other LLM-related libraries frequently handle everything, from the intricate details of LLM communication to text generation and parsing. This approach leads to several challenges:

1. **Difficulty in forming a prompt-engineering ecosystem.**
2. **High dependence on LLM, making it vulnerable to LLM changes and evolution.**
3. **Complex implementation with low customizability.**

## Solutions

To address these challenges, PromptoGen offers the following classes and interfaces:

1. **`Prompt` Data Class**: **Fostering a prompt engineering ecosystem** 
    - Defines basic LLM communication information (name, description, input/output info, template, examples).
2. **`TextLLM` Interface**: **Ensuring independence from LLM implementations**
    - Communication with LLM is through the `TextLLM` interface.
3. **`PromptFormatter` Interface**: **Enhancing customizability**
    - Users can define any formatter.
    - Generates prompt strings from `Prompt` and input.
    - Converts LLM text output to Python data structures.

PromptoGen relies solely on the data class library `Pydantic`, ensuring a robust design that remains resilient to LLM advancements.

By utilizing PromptoGen, **there's no longer a need to implement the processes that commonly convert between strings and Python objects without relying on LLM**.

## Benefits for Users

- **Modularity**: Freedom to combine.
- **Extensibility**: Ability to add custom formatters and parsers.
- **Independence**: Unaffected by new models or libraries.
- **Maintainability**: Simplified management and troubleshooting.
- **Development Efficiency**: No need to change the implementation for each LLM

## Limitations of PromptoGen

PromptoGen is designed prioritizing efficiency, simplicity, and reliability. Based on this philosophy, the tool deliberately does not support the following functionalities or characteristics:

1. **Direct Communication with LLM**:  
   PromptoGen doesn't directly support LLM communication. Instead, it emphasizes supporting interfaces and data conversion to enable efficient and natural communication.

2. **Integration of a Version Manager for Prompt Management**:  
   To avoid added complexities, the tool doesn't provide features for managing prompt versions.

3. **Optimization for Specific LLM Implementations**:  
   PromptoGen is designed to remain independent of any particular LLM implementation. This ensures it can flexibly adapt to future LLM changes or developments, serving its role as an autonomous library.

## Operating Environment

Python 3.8 or higher

# Installation

```sh
pip install promptogen
```

# Importing
```python
import promptogen as pg
```

# How to Use

## Creating your Prompt

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

## Saving the Prompt

```python
summarizer.to_json_file("summarizer.json")
```

## Loading the Prompt

```python
import promptogen as pg

summarizer = pg.Prompt.from_json_file("summarizer.json")
```

For more information, please refer to [Prompt](https://promptogen.zawakin.dev/getting-started/prompt).

## Format your Prompt as a String

To send an instance of the `Prompt` class to the LLM (Large Language Model) in actual use, you need to convert it into a string. With PromptoGen, you can use `pg.PromptFormatter` to convert the prompt into a string in any desired format.

```python
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

## Parsing Outputs from Large Language Models

After receiving the prompt string as input, you obtain an output from a large language model (like GPT-3.5, GPT-4).

LLM Output:

```console
summary: "This is a summary of the text."
keywords: ['sample', 'text', 'summarize']
```

You can parse this output as:

```python
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

## TextLLM: Flexible LLM Integration

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

For more information, please refer to [TextLLM](https://promptogen.zawakin.dev/getting-started/text-llm).

## PromptRunner: Execute Prompts Efficiently

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

`pg.PromptRunner` is a key tool for making prompt execution more intuitive and efficient using PromptoGen.

For more information, please refer to [PromptRunner](https://promptogen.zawakin.dev/getting-started/prompt-runner).

# Quick Start Guide

Please refer to the [Quick Start Guide](https://promptogen.zawakin.dev/getting-started/quickstart).

# Application Examples

Refer to [Application Examples](https://promptogen.zawakin.dev/examples).

- [Translation Interceptor](https://promptogen.zawakin.dev/examples/translation-interceptor.md)
- [Auto Prompt Generation](https://promptogen.zawakin.dev/examples/context-qa.md)
- [LLM I/O Inferences Generation](https://promptogen.zawakin.dev/examples/context-qa-reasoning.md)

# Dependent Libraries

PromptoGen only depends on [Pydantic](https://docs.pydantic.dev/latest/) to define the data class.

# Limitations

- With updates to PromptoGen, compatibility with prompts outputted in JSON may be lost.
- The large language models tested for operation are OpenAI's `gpt-3.5-turbo`, `gpt-4`, and Meta's `Llama 2`. Other large language models have not been tested for operation. In particular, there may be cases where the parser does not work correctly, so please be cautious.

# Contribution

Bug reports, proposals for new features, pull requests, etc., are all welcome! For more details, please see [Contribution](.github/CONTRIBUTING.md).

# License

MIT License
