from typing import List
import promptgen as pg
from datasets import load_dataset

label_to_emotion = {
    0: 'anger',
    1: 'joy',
    2: 'optimism',
    3: 'sadness',
}

dataset = load_dataset("tweet_eval", "emotion")


class TweetEvalEmotionDataset:
    """TweetEval Emotion Dataset
    ref. https://huggingface.co/datasets/tweet_eval
    """
    def __init__(self, seed: int = 0, train_size: int = 4, test_size: int = 50):
        self.seed = seed
        self.train_size = train_size
        self.test_size = test_size

    def load_dataset(self, mode: str, size: int) -> List[pg.Example]:
        data = dataset[mode].shuffle(seed=self.seed)[:size]

        examples=[
            pg.Example(input={'text': text}, output={'emotion': label_to_emotion[label]})
            for text, label in zip(data['text'], data['label'])
        ]

        return examples

    def load_train_dataset(self) -> List[pg.Example]:
        return self.load_dataset('train', self.train_size)

    def load_test_dataset(self) -> List[pg.Example]:
        return self.load_dataset('test', self.test_size)
