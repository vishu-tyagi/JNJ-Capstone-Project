import os
import gc
import logging
import pickle
from pathlib import Path
from typing import Optional

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

from capstone.config import CapstoneConfig
from capstone.data_access import DataClass
from capstone.features.helpers import (spacy_init, spacy_normalize, tfidf_init)
from capstone.utils import timing
from capstone.utils.constants import (
    DATA_DIR,
    MODEL_DIR,
    TEXT,
    TARGET,
    SPLIT,
    DEVELOP,
    TEST
)

logger = logging.getLogger(__name__)


class Features():
    def __init__(self, config: CapstoneConfig):
        self.config = config
        self.current_path = Path(os.getcwd()) if not config.CURRENT_PATH else config.CURRENT_PATH
        self.data_path = Path(os.path.join(self.current_path, DATA_DIR))
        self.model_path = Path(os.path.join(self.current_path, MODEL_DIR))

        self.mlb = MultiLabelBinarizer()
        self.nlp = spacy_init()
        self.vectorizer = tfidf_init()
        self.vectorizer_path = os.path.join(self.model_path, config.TFIDF_FILE_NAME)

    # def save(self):
    #     processor_path = os.path.join(self.model_path, self.processor_name)
    #     logger.info(f"Saving processor to {processor_path}")
    #     pickle.dump(self.processor, open(processor_path, "wb"))

    # @timing
    # def load(self):
    #     processor_path = os.path.join(self.model_path, self.processor_name)
    #     logger.info(f"Loading processor from {processor_path}")
    #     self.processor = pickle.load(open(processor_path, "rb"))

    @timing
    def build(self, df: pd.DataFrame):
        self.mlb.fit(df[TARGET])
        Y = self.mlb.transform(df[TARGET])
        df = df.join(
            pd.DataFrame(
                self.mlb.transform(df[TARGET]),
                columns=self.mlb.classes_,
                index=df.index
            )
        ).copy()
        dev, test, _, _ = train_test_split(
            df, Y, test_size=.1, shuffle=True, random_state=64
        )
        dev, test = self.fit_transform(dev), self.transform(test)
        dev[SPLIT], test[SPLIT] = DEVELOP, TEST
        df = pd.concat([dev, test], ignore_index=True).copy()
        return df

    @timing
    def fit(self, df: pd.DataFrame):
        df = self.clean(df)
        self.vectorizer.fit(df[TEXT].values)
        return self

    @timing
    def transform(self, df: pd.DataFrame):
        df = self.clean(df)
        X = self.vectorizer.transform(df[TEXT].values)
        X = pd.DataFrame(X.toarray(), columns=self.vectorizer.get_feature_names_out())
        df = pd.concat([df.reset_index(drop=True), X], axis=1).copy()
        return df

    @timing
    def fit_transform(self, df: pd.DataFrame):
        return self.fit(df).transform(df)

    @timing
    def clean(self, df: pd.DataFrame):
        df = df.copy()
        df.reset_index(drop=True, inplace=True)
        logger.info("Cleaning text")
        # Remove HTML
        df[TEXT] = df[TEXT].str.replace("<[^<]+?>", " ", regex=True)
        # Remove emojis
        df[TEXT] = df[TEXT].astype(str).apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
        # Remove punctuation
        df[TEXT].str.replace(r"[^\w\s]", "", regex=True)
        # Conver to lower case
        df[TEXT] = df[TEXT].str.lower()
        # Remove URLs
        df[TEXT] = df[TEXT].str.replace(r"http\S+|www.\S+", "", regex=True)
        logger.info("Applying language model")
        df[TEXT] = pd.Series(self.nlp.pipe(df[TEXT].values))
        logger.info("Applying lemmatization and removing stopwords")
        df[TEXT] = \
            df[TEXT] \
            .apply(lambda x: spacy_normalize(x, self.nlp.Defaults.stop_words)) \
            .apply(lambda x: " ".join(x))
        return df
