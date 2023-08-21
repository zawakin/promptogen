# PromptoGen

<a href="/" target="_blank"><img src="https://promptogen.zawakin.dev/img/logo-light-mode.svg"></a>

<p align="center">
    <em>Bridging LLMs and Python Seamlessly.</em>
</p>

<p align="center">
<a href="https://github.com/zawakin/promptogen/releases" target="_blank">
    <img src="https://img.shields.io/github/release/zawakin/promptogen" alt="Releases">
</a>

<a href="https://github.com/zawakin/promptogen/actions/workflows/test.yml?query=branch%3Amain+event%3Apush" target="_blank">
    <img src="https://github.com/zawakin/promptogen/actions/workflows/test.yml/badge.svg" alt="Test">
</a>
<a href="https://pypi.org/project/promptogen" target="_blank">
    <img src="https://img.shields.io/pypi/v/promptogen?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/promptogen" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/promptogen.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

----

**Documentation**: https://promptogen.zawakin.dev

**Source Code**: https://github.com/zawakin/promptogen

**Getting Started**: https://promptogen.zawakin.dev/getting-started/installation


- [en - English](https://promptogen.zawakin.dev)
- [ja - 日本語](https://promptogen.zawakin.dev/ja)

----

## PromptoGen: Achieving efficient and expandable communication with LLM

## 🚀 Vision
**"Seamlessly bridge the gap between LLM and Python, ensuring efficient, future-ready communication."**

## 💡 Key Challenges in LLM Libraries:
- **Lack of an ecosystem for prompt engineering**, making prompt creation and sharing difficult.
- **Strong dependency on specific LLM versions**, making them vulnerable to LLM updates.
- **Complex implementations**, hindering customization.

## 🎯 Why Choose PromptoGen?
1. **Seamless Conversion between LLM I/O and Python Objects**: Streamlining LLM interactions.
2. **Flexible & Unique Interface**: Guaranteeing user customizability and extensibility.
3. **Future-Proof Design**: Stay ahead with reduced dependency on LLM evolutions.

**Compared to Other Libraries**: Many are tied to specific LLM versions, lacking the adaptability that PromptoGen offers. With a dependency only on the `Pydantic` data class library, PromptoGen serves as the ideal bridge between LLM strings and Python objects.

## 🛠️ Core Features:
- **`Prompt` Data Class**: Standardizing LLM communication and supporting prompt engineering.
- **`TextLLM` Interface**: Independence from LLM specifics.
- **`PromptFormatter` Interface**: High customizability for users.

## 🎉 Benefits:
- 🧩 **Modular & Extendable**: Flexibly mix, match, and add custom components.
- 🛡️ **Future-Proof**: Stand strong against new model updates.
- 🔧 **Maintainability**: Ensuring easy debugging and minimal adjustments for different LLMs.

## ⚠️ Unsupported Features:
- **Direct LLM Communication**: We prioritize efficient interfacing over direct LLM conversations.
- **Prompt Version Management**: To keep things streamlined, we avoid adding versioning complexities.
- **Specific LLM Optimization**: Our focus is on adaptability across LLMs rather than optimizing for any single one.

## 📚 Learn More
Dive deep into the [documentation](https://promptogen.zawakin.dev) for a comprehensive understanding.


----

# Requirements
Python 3.8 or above

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

- [Translation Interceptor](https://promptogen.zawakin.dev/examples/translation-interceptor)
- [Auto Prompt Generation](https://promptogen.zawakin.dev/examples/context-qa)
- [LLM I/O Inferences Generation](https://promptogen.zawakin.dev/examples/context-qa-reasoning)

# Dependent Libraries

PromptoGen only depends on [Pydantic](https://docs.pydantic.dev/latest/) to define the data class.

# Limitations

- With updates to PromptoGen, compatibility with prompts outputted in JSON may be lost.
- The large language models tested for operation are OpenAI's `gpt-3.5-turbo`, `gpt-4`, and Meta's `Llama 2`. Other large language models have not been tested for operation. In particular, there may be cases where the parser does not work correctly, so please be cautious.

# Contribution

Bug reports, proposals for new features, pull requests, etc., are all welcome! For more details, please see [Contribution](.github/CONTRIBUTING.md).

# License

MIT License
