import sys
import logging

from capstone.api import fetch


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    try:
        if sys.argv[1] == 'fetch':
            fetch()
    except IndexError:
        raise ValueError("Call to API requires an endpoint")
