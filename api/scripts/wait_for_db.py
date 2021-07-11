import logging
from os import environ
import time

from psycopg2 import connect

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 5


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def wait() -> None:
    logger.info("Retrieving connection to database ...")
    # Obligatory wait
    time.sleep(3)

    try:
        connection = connect(
            host=environ["DB_HOST"],
            port=environ["DB_PORT"],
            user=environ["DB_USER"],
            database="postgres",
        )
    except Exception as e:
        logger.error(e)
        raise e
    logger.info("Successfully connected to database")

    try:
        cursor = connection.cursor()
    except Exception as e:
        logger.error(e)
        raise e
    logger.info("Successfully retrieved cursor to database")

    try:
        # Try to create session to check if DB is awake
        cursor.execute("SELECT 1")
        logger.info("Successfully retrieved connection session to database")
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    wait()
