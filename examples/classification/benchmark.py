from typing import List
# from tenacity import retry, stop_after_attempt
from examples.base import make_json_path
from examples.llm.openai_util import generate_text_by_text_openai_api
from examples.classification.dataset_loader import TweetEvalEmotionDataset

import promptgen as pg
import time


def run_benchmark_prompt(prompt_to_test: pg.Prompt, test_examples: List[pg.Example], output_key: str):
    total = 0
    correct = 0

    for example in test_examples:
        time.sleep(3)

        # @retry(stop=stop_after_attempt(2))
        def f() -> pg.Value:
            return prompt_runner.run_prompt(prompt_to_test,  example.input)

        try:
            resp = f()
        except Exception as e:
            print(f'Error: {e}; skipping...')
            total += 1
            continue

        total += 1

        got = resp[output_key]
        expected = example.output[output_key]

        if got == expected:
            correct += 1
        else:
            print(f'got {got} expected {expected}, input: {example.input}')

        print(f'Total: {total}, Correct: {correct}, Accuracy: {correct/total}')


if __name__ == '__main__':
    formatter = pg.KeyValuePromptFormatter()
    llm = pg.TextBasedLLMWrapper(generate_text_by_text=lambda s: generate_text_by_text_openai_api(s, 'gpt-3.5-turbo'))
    prompt_runner = pg.TextBasedPromptRunner(llm=llm, formatter=formatter)

    dataset = TweetEvalEmotionDataset(seed=43)

    prompt_to_test = pg.Prompt.from_json_file(make_json_path(dataset.attributes.name + '_with_reason.json'))

    test_examples = dataset.load_test_dataset()

    run_benchmark_prompt(prompt_to_test, test_examples, dataset.attributes.output_key)
