from typing import Dict, List

from datasets import DatasetDict, load_dataset
from pydantic import BaseModel

import promptogen as pg


class DatasetAttributes(BaseModel):
    input_key: str
    output_key: str
    description: str
    background: str
    name: str


class DatasetLoader:
    def __init__(
        self,
        seed: int,
        train_size: int,
        test_size: int,
        dataset: DatasetDict,
        attributes: DatasetAttributes,
        label_map: Dict[int, str],
    ):
        self.seed = seed
        self.train_size = train_size
        self.test_size = test_size
        self.dataset = dataset
        self.attributes = attributes
        self.label_map = label_map

    def load_dataset(self, mode: str, size: int) -> List[pg.IOExample]:
        data = self.dataset[mode].shuffle(seed=self.seed)[:size]

        examples = [
            pg.IOExample(
                input={self.attributes.input_key: text}, output={self.attributes.output_key: self.label_map[label]}
            )
            for text, label in zip(data["text"], data["label"])
        ]

        return examples

    def load_train_dataset(self) -> List[pg.IOExample]:
        return self.load_dataset("train", self.train_size)

    def load_test_dataset(self) -> List[pg.IOExample]:
        return self.load_dataset("test", self.test_size)


class TweetEvalEmotionDataset(DatasetLoader):
    """TweetEval Emotion Dataset
    ref. https://huggingface.co/datasets/tweet_eval
    """

    def __init__(self, seed: int = 0, train_size: int = 4, test_size: int = 50):
        attributes = DatasetAttributes(
            name="tweet_eval_emotion",
            input_key="text",
            output_key="emotion",
            description="Classify the emotion of a tweet, as anger, joy, optimism, or sadness",
            background='(text: str) -> (emotion: str); emotion should be "anger", "joy", "optimism", or "sadness" depending on the tweet. add examples for all four emotions.',
        )
        label_map = {
            0: "anger",
            1: "joy",
            2: "optimism",
            3: "sadness",
        }
        super().__init__(seed, train_size, test_size, load_dataset("tweet_eval", "emotion"), attributes, label_map)


class IMDbSentimentDataset(DatasetLoader):
    """IMDb Sentiment Dataset
    ref. https://huggingface.co/datasets/imdb"""

    def __init__(self, seed: int = 0, train_size: int = 4, test_size: int = 50):
        attributes = DatasetAttributes(
            name="imdb_entiment",
            input_key="review",
            output_key="sentiment",
            description="Classify the sentiment of a movie review, as positive or negative. sentiment must be positive or negative depending on the review.",
            background='(review: str) -> (sentiment: str); sentiment should be "positive" or "negative". Add examples for both positive and negative reviews.',
        )
        label_map = {
            0: "negative",
            1: "positive",
        }
        super().__init__(seed, train_size, test_size, load_dataset("imdb"), attributes, label_map)
