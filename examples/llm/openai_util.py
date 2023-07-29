import openai
import os

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

from colorama import Fore, Style, init

init(autoreset=True)


def generate_text_by_text_openai_api(text: str, model: str, verbose=True) -> str:
    if verbose:
        print(Fore.BLUE + '-- input --')
        print(Fore.BLUE + text)
    resp = openai.ChatCompletion.create(model=model, messages=[
        {'role': 'user', 'content': text}
    ], max_tokens=2048, timeout=5)
    if not isinstance(resp, dict):
        raise Exception(resp)
    raw_resp = resp['choices'][0]['message'].get('content', '')
    if verbose:
        print(Fore.GREEN + '-- output --')
        print(Fore.GREEN + raw_resp)
    return raw_resp
