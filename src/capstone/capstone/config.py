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
        "ANVISA RDC 665_ On the Good Manufacturing Practices of Medical Devices.xml",
        "Regulatory Requirements.xlsx",
        "jnj_hygiene_ft_training_data.csv"
    ]

    # OpenAI beta key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_BETA")
