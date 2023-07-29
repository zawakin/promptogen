from tenacity import retry, stop_after_attempt
from base import make_json_path
from examples.llm.openai_util import generate_text_by_text_openai_api
from examples.tweet_eval_emotion.dataset_loader import TweetEvalEmotionDataset

import promptgen as pg
import time


def run_benchmark_prompt(prompt_to_test: pg.Prompt):
    total = 0
    correct = 0

    for example in test_examples:
        time.sleep(3)

        try:
            # @retry(stop=stop_after_attempt(2))
            def f() -> pg.Value:
                return prompt_runner.run_prompt(prompt_to_test,  example.input)
            resp = f()
        except Exception as e:
            print(f'Error: {e}; skipping...')
            total += 1
            continue

        total += 1

        got = resp['emotion']
        expected = example.output['emotion']

        if got == expected:
            correct += 1
        else:
            print(f'got {got} expected {expected}, text: {example.input["text"]}')

        print(f'Total: {total}, Correct: {correct}, Accuracy: {correct/total}')


if __name__ == '__main__':
    formatter = pg.KeyValuePromptFormatter()
    llm = pg.TextBasedLLMWrapper(generate_text_by_text=lambda s: generate_text_by_text_openai_api(s, 'gpt-3.5-turbo'))
    prompt_runner = pg.TextBasedPromptRunner(llm=llm, formatter=formatter)

    prompt_to_test = pg.Prompt.from_json_file(make_json_path('tweet_eval_emotion_classifier_with_reason.json'))

    test_examples = TweetEvalEmotionDataset(seed=43).load_test_dataset()

    run_benchmark_prompt(prompt_to_test)
