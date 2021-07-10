import logging
from os import environ

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errorcodes import DUPLICATE_DATABASE

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from wait_for_db import wait

logging.basicConfig()
logging.root.setLevel(logging.INFO)
module_path = ".".join(__file__.rstrip(".py").lstrip(".").lstrip("/").split("/"))
logger = logging.getLogger(module_path)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 5


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def create_db():
    db_name = environ["DB_NAME"]
    connection = connect(
        host=environ["DB_HOST"],
        port=environ["DB_PORT"],
        user=environ["DB_USER"],
        database="postgres",
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    try:
        logger.info("Creating database %s", db_name)
        cursor.execute(f"CREATE DATABASE {db_name};")
        logger.info("Database %s created successfully", db_name)
    except Exception as e:
        if e.pgcode == DUPLICATE_DATABASE:
            logger.info("Database %s already created, nothing to do", db_name)
        else:
            logger.error(e)
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    wait()
    create_db()
