from spacy import load as spacy_load
from spacy.tokens.doc import Doc
from spacy.language import Language
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
import nltk

from capstone.config import CapstoneConfig


def stopwords_init(config: CapstoneConfig = CapstoneConfig) -> Language:
    """_summary_
    Args:
        config (CapstoneConfig): _description_
    Returns:
        Language: _description_
    """
    stopwords = nltk.corpus.stopwords.words("english")
    stopwords.extend(config.STOPWORDS_TO_ADD)
    return stopwords


def tfidf_init(config: CapstoneConfig = CapstoneConfig) -> TfidfVectorizer:
    char = "char" in config.TFIDF_ANALYZERS
    word = "word" in config.TFIDF_ANALYZERS

    if char and not word:
        vectorizer = FeatureUnion([
            ("char", TfidfVectorizer(**config.TFIDF_CHAR_PARAMETERS))
        ])
    elif not char and word:
        vectorizer = FeatureUnion([
            ("word", TfidfVectorizer(**config.TFIDF_WORD_PARAMETERS))
        ])
    else:
        vectorizer = FeatureUnion([
            ("char", TfidfVectorizer(**config.TFIDF_CHAR_PARAMETERS)),
            ("word", TfidfVectorizer(**config.TFIDF_WORD_PARAMETERS))
        ])
    return vectorizer
