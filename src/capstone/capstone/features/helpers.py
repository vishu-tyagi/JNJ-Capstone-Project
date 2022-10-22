from spacy import load as spacy_load
from spacy.tokens.doc import Doc
from spacy.language import Language
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion

from capstone.config import CapstoneConfig


def spacy_init(config: CapstoneConfig = CapstoneConfig) -> Language:
    """_summary_
    Args:
        config (CapstoneConfig): _description_
    Returns:
        Language: _description_
    """
    nlp = spacy_load(config.NLP_MODEL)
    # nlp.Defaults.stopwords |= config.STOPWORDS_TO_ADD
    # nlp.Defaults.stopwords -= config.STOPWORDS_TO_DELETE
    return nlp


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


def spacy_normalize(doc: Doc, stop_words: set[str]) -> list[str]:
    tokens = []
    for token in doc:
        if token.pos_ in ["PUNCT", "X"]:
            pass
        elif token.pos_ != "PRON":
            tokens.append(token.lemma_.lower().strip())
        else:
            tokens.append(token.lower_)

    tokens = [token for token in tokens if token not in stop_words]
    return tokens
