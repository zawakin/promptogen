from base import make_json_path

from examples.llm.openai_util import generate_text_by_text_openai_api
from examples.tweet_eval_emotion.dataset_loader import TweetEvalEmotionDataset

import promptgen as pg


def setup_base_prompt() -> pg.Prompt:
    # ref. https://huggingface.co/datasets/tweet_eval
    resp = prompt_runner.run_prompt(collection['PromptCreator'], {
        'purpose': "Classify emotion of tweet; (text: str) -> (emotion: str); 'emotion' must be one of anger, joy, optimism, sadness.",
        'background': "add examples of these four emotions",
    })
    return pg.Prompt.from_dict(resp['prompt'])


def setup_reasoning_prompt(prompt: pg.Prompt) -> pg.Prompt:
    reasoning_extractor = pg.LLMReasoningExtractor(text_based_llm=llm, explanation_template="This is because ... So the answer is ...")
    reasoning_transformer = pg.PromptWithReasoningTransformer(reasoning_extractor)
    prompt_with_reasoning = reasoning_transformer.transform_prompt(prompt)
    return prompt_with_reasoning


if __name__ == '__main__':
    formatter = pg.KeyValuePromptFormatter()
    llm = pg.TextBasedLLMWrapper(generate_text_by_text=lambda s: generate_text_by_text_openai_api(s, 'gpt-3.5-turbo'))
    prompt_runner = pg.TextBasedPromptRunner(llm=llm, formatter=formatter)
    collection = pg.PromptCollection(load_predefined=True)

    # create base prompt without reasoning
    emotion_classifier = setup_base_prompt()

    # load dataset
    # train_examples = TweetEvalEmotionDataset(seed=43).load_train_dataset()
    # emotion_classifier = emotion_classifier.update(examples=train_examples)

    emotion_classifier.to_json_file(make_json_path('tweet_eval_emotion_classifier.json'))

    # create prompt with reasoning
    emotion_classifier_reasoning = setup_reasoning_prompt(emotion_classifier)
    emotion_classifier_reasoning.to_json_file(make_json_path('tweet_eval_emotion_classifier_with_reason.json'))
