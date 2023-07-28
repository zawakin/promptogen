# %%
from typing import List
import promptgen as pg
import time
collection = pg.PromptCollection(load_predefined=True)
config = pg.PromptFormatterConfig()

force_setup = True

formatter_mode = 'key_value'

if formatter_mode == 'key_value':
    formatter = pg.KeyValuePromptFormatter(config=config)
elif formatter_mode == 'json':
    formatter = pg.JsonPromptFormatter(strict=False, config=config)
else:
    raise ValueError(f'Unknown formatter mode: {formatter_mode}')

#%%
import openai
import os

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")


def generate_llm_response(prompt: str, model: str) -> str:
    resp = openai.ChatCompletion.create(model=model, messages=[
        {'role': 'user', 'content': prompt}
    ], max_tokens=2048, timeout=5)
    if not isinstance(resp, dict):
        raise Exception(resp)
    return resp['choices'][0]['message'].get('content', '')


def run_prompt(prompt: pg.Prompt, input_value: pg.Value) -> pg.Value:
    raw_req = formatter.format_prompt(prompt, input_value=input_value)
    raw_resp = generate_llm_response(raw_req, 'gpt-3.5-turbo-16k')
    print(raw_req)
    print(raw_resp)
    resp = formatter.parse(prompt, raw_resp)
    return resp

#%%


label_to_emotion = {
    0: 'anger',
    1: 'joy',
    2: 'optimism',
    3: 'sadness',
}

# emotion_classifier = setup_prompt()
# emotion_classifier.to_json_file('tweet_eval_emotion_classifier.json')


#%%


def setup_base_prompt() -> pg.Prompt:
    try:
        emotion_classifier = pg.Prompt.from_json_file('tweet_eval_emotion_classifier.json')
        return emotion_classifier
    except FileNotFoundError:
        pass

    # ref. https://huggingface.co/datasets/tweet_eval
    resp = run_prompt(collection['PromptCreator'], {
        'purpose': "Classify emotion of tweet; (text: str) -> (label: str); label must be one of anger, joy, optimism, sadness.",
        'background': "",
    })
    result = pg.Prompt.from_dict(resp['prompt'])
    result.to_json_file('tweet_eval_emotion_classifier.json')
    return result


emotion_classifier = setup_base_prompt()


from datasets import load_dataset

dataset = load_dataset("tweet_eval", "emotion")


def setup_reasoning_prompt(base_prompt: pg.Prompt) -> pg.Prompt:
    if not force_setup:
        try:
            emotion_classifier_reasoning = pg.Prompt.from_json_file('tweet_eval_emotion_classifier_with_reason.json')
            return emotion_classifier_reasoning
        except FileNotFoundError:
            pass

    train_data = dataset['train'].shuffle(seed=43)[:4] # type: ignore
    train_text, train_label = train_data['text'], train_data['label'] # type: ignore

    examples = [
        pg.Example(
            input={
                'text': text,
            },
            output={
                'emotion': label_to_emotion[label],
            },
        )
        for text, label in zip(train_text, train_label)
    ]
    emotion_classifier = base_prompt.update(examples=examples)

    explanation_generator = pg.ExplanationGenerator(generate_llm_response=lambda s: generate_llm_response(s, 'gpt-4'))
    reasoning_prompt_transformer = pg.ReasoningPromptTransformer(explanation_generator)

    emotion_classifier_reasoning = reasoning_prompt_transformer.transform_prompt(emotion_classifier)
    emotion_classifier_reasoning.to_json_file('tweet_eval_emotion_classifier_with_reason.json')
    return emotion_classifier_reasoning


emotion_classifier = setup_base_prompt()
emotion_classifier_reasoning = setup_reasoning_prompt(emotion_classifier)

#%%
d = dataset['test'].shuffle(seed=43)[:50] # type: ignore

texts = d['text']
labels = d['label']

total = 0
correct = 0

for text, label in zip(texts, labels):
    time.sleep(3)
    def f() -> pg.Value:
        resp = run_prompt(emotion_classifier_reasoning,  {
            'text': text,
        })
        return resp

    try:
        resp = f()
    except Exception as e:
        print(f'Error: {e}; retrying...')
        time.sleep(5)

        try:
            resp = f()
        except Exception as e:
            print(f'Error: {e}; skipping...')
            total += 1
            continue

    total += 1
    label_str = label_to_emotion[label]
    if resp['emotion'] == label_str:
        correct += 1
    else:
        expected_sentiment = label_str
        print(f'got {resp["emotion"]} expected {expected_sentiment}, text: {text}')

    print(f'Total: {total}, Correct: {correct}, Accuracy: {correct/total}')

#%%
