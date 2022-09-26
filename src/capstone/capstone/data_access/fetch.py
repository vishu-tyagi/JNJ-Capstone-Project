import os
import logging
from pathlib import Path
from sys import prefix

import boto3

from capstone.config import CapstoneConfig
from capstone.data_access.helpers import s3_download
from capstone.utils.constants import (
    DATA_DIR,
    MODEL_DIR,
    REPORTS_DIR
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

    def _fetch(self):
        logger.info(f"Downloading s3://{self.s3_bucket}")
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        s3_download(s3_client, self.s3_bucket, self.config.S3_BUCKET_RELEVANT_FILES, self.data_path)

    def build(self):
        self._fetch()
        logger.info(
            f"Data available at {self.data_path}"
        )
