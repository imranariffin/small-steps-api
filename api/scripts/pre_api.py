import logging

from wait_for_db import wait

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Preparing api ...")
    wait()
    logger.info("api successfully prepared")
