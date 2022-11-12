import os
from pathlib import Path
import logging
import itertools

import boto3
import pandas as pd

from capstone.config import CapstoneConfig
from capstone.data_access.helpers import s3_download
from capstone.utils.constants import (
    DATA_DIR,
    MODEL_DIR,
    REPORTS_DIR,
    XLSX_DATA,
    XLSX_SHEET,
    TEXT,
    TARGET,
    IS_MAPPED,
    IS_MAPPED_TRUE
)

logger = logging.getLogger(__name__)


class DataClass():
    def __init__(self, config: CapstoneConfig):
        self.config = config
        self.s3_bucket = config.S3_BUCKET

        self.current_path = Path(os.getcwd()) if not config.CURRENT_PATH else config.CURRENT_PATH
        self.data_path = Path(os.path.join(self.current_path, DATA_DIR))
        self.model_path = Path(os.path.join(self.current_path, MODEL_DIR))
        self.reports_path = Path(os.path.join(self.current_path, REPORTS_DIR))

    def make_dirs(self):
        dirs = [
            self.data_path,
            self.model_path,
            self.reports_path
        ]
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created data directory {self.data_path}")
        logger.info(f"Created model directory {self.model_path}")
        logger.info(f"Created reports directory {self.reports_path}")

    def fetch(self):
        logger.info(f"Downloading s3://{self.s3_bucket}")
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        s3_download(s3_client, self.s3_bucket, self.config.S3_BUCKET_RELEVANT_FILES, self.data_path)
        logger.info(f"Data available at {self.data_path}")

    def build(self):
        xls = pd.ExcelFile(os.path.join(self.data_path, XLSX_DATA))
        df = pd.read_excel(xls, XLSX_SHEET)
        df = df[df[IS_MAPPED].isin([IS_MAPPED_TRUE])].copy()
        df = df[[TEXT, TARGET]].copy()
        df[TARGET] = \
            df[TARGET].str.lower() \
            .apply(lambda x: list(x.split("\n"))) \
            .apply(lambda x: [y.split(",") for y in x]) \
            .apply(lambda x: list(itertools.chain(*x))) \
            .apply(lambda x: [y.strip().replace("-", " ") for y in x if y.strip() != ""]) \
            .apply(lambda x: sorted(x)) \
            .apply(lambda x: ", ".join(x))
        df = df.groupby([TEXT], as_index = False).agg({TARGET: ", ".join}).copy()
        df[TARGET] = \
            df[TARGET] \
            .apply(lambda x: x.split(", ")) \
            .apply(lambda x: list(set(x))) \
            .apply(lambda x: sorted(x))
        return df
