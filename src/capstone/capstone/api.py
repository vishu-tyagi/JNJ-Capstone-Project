import logging

from capstone.config import CapstoneConfig
from capstone.data_access import DataClass
from capstone.utils import timing

logger = logging.getLogger(__name__)


@timing
def fetch(config: CapstoneConfig = CapstoneConfig) -> None:
    logger.info("Fetching data...")
    data = DataClass(config)
    data.make_dirs()
    data.build()
    return
