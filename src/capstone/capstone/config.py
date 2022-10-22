import os


class CapstoneConfig():
    # S3 bucket for fetching raw data
    S3_BUCKET = "jnj-capstone"
    CURRENT_PATH = None   # will be set to working directory by os.getcwd()

    # Files to download from S3 bucket
    S3_BUCKET_RELEVANT_FILES = [
        "eudralex_chapter4_documentation.csv",
        "jnj_hygiene_ft_training_data.csv",
        "jnj_hygiene_regulation_examples.csv",
        "Regulatory Requirements - Hygiene.pkl",
        "trainingdata.jsonl",
        "jnj_hygiene_ft_training_data_prepared.jsonl",
        "EudraLex - Chapter 4 - Documentation.xlsx",
        "chapter4_01_2011_en_0.xml",
        "ANVISA RDC 665_ On the Good Manufacturing Practices of Medical Devices.xml"
    ]

    # OpenAI beta key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_BETA")

    # Features
    NLP_MODEL = "en_core_web_lg"
    NLP_STOPWORDS_TO_ADD: set[str] = {}
    NLP_STOPWORDS_TO_DELETE: set[str] = {}

    TFIDF_FILE_NAME = "vectorizer.pickle"
    TFIDF_ANALYZERS = {"word"}
    TFIDF_CHAR_PARAMETERS = {
        "analyzer": "char",
        "ngram_range": (3, 3),
        "max_features": 500,
        "min_df": 0.001,
        "max_df": 0.6
    }
    TFIDF_WORD_PARAMETERS = {
        "analyzer": "word",
        "ngram_range": (2, 3),
        "max_features": 3000,
        "min_df": 0.005,
        "max_df": .725
    }
