import os

import openai
from dotenv import load_dotenv

from promptgen.model.llm import TextLLM

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

from colorama import Fore, init

# initialize colorama for colored output
init(autoreset=True)


class OpenAITextBasedLLM(TextLLM):
    def __init__(self, model: str, verbose=True):
        self.model = model
        self.verbose = verbose

    def generate(self, text: str) -> str:
        return generate_chat_completion(text, self.model, verbose=self.verbose)


def generate_chat_completion(text: str, model: str, verbose=True) -> str:
    if verbose:
        print(Fore.BLUE + "-- input --")
        print(Fore.BLUE + text)
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        max_tokens=2048,
        timeout=5,
        stream=True,
    )
    if verbose:
        print(Fore.GREEN + "-- output --")
    raw_resp = ""
    for chunk in resp:
        chunk_content = chunk["choices"][0]["delta"].get("content", "")
        raw_resp += chunk_content

        if verbose:
            print(Fore.GREEN + chunk_content, end="")
    if verbose:
        print()

    return raw_resp
