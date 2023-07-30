import typer

import promptgen as pg
from examples.base import make_json_path
from examples.classification.dataset_loader import DatasetLoader, IMDbSentimentDataset, TweetEvalEmotionDataset
from examples.llm.openai_util import generate_text_by_text_openai_api

app = typer.Typer()


@app.command("tweet_eval_emotion")
def run_tweet_eval_emotion():
    dataset = TweetEvalEmotionDataset(seed=43)
    setup_prompt_by_dataset(dataset)


@app.command("imdb_sentiment")
def run_imdb_sentiment():
    dataset = IMDbSentimentDataset(seed=43)
    setup_prompt_by_dataset(dataset)


formatter = pg.KeyValuePromptFormatter()
llm = pg.TextBasedLLMWrapper(generate_text_by_text=lambda s: generate_text_by_text_openai_api(s, "gpt-3.5-turbo"))
prompt_runner = pg.TextBasedPromptRunner(llm=llm, formatter=formatter)
collection = pg.PromptCollection(load_predefined=True)


def setup_base_prompt(input_value: pg.Value) -> pg.Prompt:
    resp = prompt_runner.run_prompt(collection["PromptCreator"], input_value=input_value)
    return pg.Prompt.from_dict(resp["prompt"])


def setup_reasoning_prompt(prompt: pg.Prompt) -> pg.Prompt:
    reasoning_extractor = pg.LLMReasoningExtractor(
        text_based_llm=llm, explanation_template="This is because ... So the answer is ..."
    )
    reasoning_transformer = pg.PromptWithReasoningTransformer(reasoning_extractor)
    prompt_with_reasoning = reasoning_transformer.transform_prompt(prompt)
    return prompt_with_reasoning


def setup_prompt_by_dataset(dataset: DatasetLoader):
    # create base prompt without reasoning
    classfier_prompt = setup_base_prompt(
        {
            "description": dataset.attributes.description,
            "background": dataset.attributes.background,
        }
    )
    # emotion_classifier = emotion_classifier.update(examples=train_examples)

    classfier_prompt.to_json_file(make_json_path(dataset.attributes.name + ".json"))

    # create prompt with reasoning
    classfier_prompt_with_reasoning = setup_reasoning_prompt(classfier_prompt)
    classfier_prompt_with_reasoning.to_json_file(make_json_path(dataset.attributes.name + "_with_reason.json"))


if __name__ == "__main__":
    app()
