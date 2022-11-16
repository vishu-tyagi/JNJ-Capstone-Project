import os
import logging
import logging.config
from pathlib import Path
from typing import List

from capstone.utils import timing

logger = logging.getLogger(__name__)


@timing
def s3_download(client, bucket: str, files: List[str], out_path: Path):
    for file in files:
        client.download_file(bucket, file, os.path.join(out_path, file))
        logger.info(f"Downloaded s3://{bucket}/{file}")
