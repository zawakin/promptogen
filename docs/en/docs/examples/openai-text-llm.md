This guide explains how to implement the TextLLM using the OpenAI API with the [TextLLM Interface](../getting-started/text-llm.md).

## Installing Required Libraries

```sh
pip install promptogen openai python-dotenv colorama
```

## Setting Environment Variables

Create a `.env` file. Please refer to the [OpenAI API](https://platform.openai.com/docs/api-reference/introduction) for details on setting this up.

```shell
# .env
OPENAI_API_KEY=<your-openai-api-key>
OPENAI_ORG_ID=<your-openai-org-id>
```

## Implementing TextLLM using the OpenAI API

We use `colorama` to display colored text on the terminal.

```python
import os

import openai
from dotenv import load_dotenv

from promptogen.model.llm import TextLLM

# load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

from colorama import Fore, init

# initialize colorama for colored output
init(autoreset=True)


class OpenAITextLLM(TextLLM):
    def __init__(self, model: str, verbose=True):
        self.model = model
        self.verbose = verbose

    def generate(self, text: str) -> str:
        if self.verbose:
            print(Fore.BLUE + "-- input --")
            print(Fore.BLUE + text)
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": text}],
            max_tokens=2048,
            timeout=5,
            stream=True,
        )
        if self.verbose:
            print(Fore.GREEN + "-- output --")
        raw_resp = ""
        for chunk in resp:
            chunk_content = chunk["choices"][0]["delta"].get("content", "")
            raw_resp += chunk_content

            if self.verbose:
                print(Fore.GREEN + chunk_content, end="")
        if self.verbose:
            print()

        return raw_resp
```

## How to Use

```python
text_llm = OpenAITextLLM(model="gpt-3.5-turbo")

text = "Hello, I'm a human."
print(text_llm.generate(text))
```

```console
-- input --
Hello, I'm a human.
-- output --
Hello! How can I assist you today as an AI?
```
