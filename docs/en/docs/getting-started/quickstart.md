## Import
    
```python
--8<-- "quickstart/quickstart.py:import"
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
--8<-- "quickstart/quickstart.py:summarizer"
```

## Format the Prompt to String without Input Parameters

First, let's format the prompt to a string without input parameters.

In PromptoGen, you can flexibly create formatters to turn prompts into strings.

Here, we use a formatter named `KeyValuePromptFormatter` which outputs the input-output variables in the form `key: value`.

To format the prompt to a string without input parameters, use the `format_prompt_without_input` method.
This method takes the prompt and formatter as arguments and formats the prompt into a string.

```python
--8<-- "quickstart/quickstart.py:format_prompt_without_input"
```

Console Output:

```console
--8<-- "quickstart/output.txt:format_prompt_without_input"
```

## Format the Prompt to String with Input Parameters

Next, let's format the prompt to a string with input parameters.

Input parameters are specified using a `dict`.

To format the prompt to a string with input parameters, use the `format_prompt` method.

```python
--8<-- "quickstart/quickstart.py:format_prompt"
```

Console Output:

```console
--8<-- "quickstart/output.txt:format_prompt"
```

## Generating Output Using Large Language Models

Next, let's try generating output from a large language model.

This library does not provide functionality to generate output from large language models, but it can be achieved using the OpenAI ChatGPT API.

Here, using the OpenAI ChatGPT API, let's generate a summarized text from the input text.

In advance, set the OpenAI API Key and Organization ID as environment variables.

```python
--8<-- "quickstart/quickstart.py:text_llm"
```

`TextLLM` is an abstract class in PromptoGen to uniformly handle large language models. `pg.FunctionBasedTextLLM` is an implementation of `TextLLM` that generates output from large language models using a function.

Next, let's format the prompt with input parameters into a string and generate output from the large language model.

```python
--8<-- "quickstart/quickstart.py:generate"
```

Console Output:

```console
--8<-- "quickstart/output.txt:generate"
```

## Convert the Output to a Python Object

Next, since the LLM output is just a string, let's convert it to a Python object. By using the `formatter.parse` method, you can parse the output string from the LLM using the output parameters of the prompt. The parsing result is stored in a Python `dict`.

```python
--8<-- "quickstart/quickstart.py:parse"
```

Console Output:

```console
--8<-- "quickstart/output.txt:parse"
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
