import logging
import typing as t

from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


engine = create_engine(
    environ["DATABASE_URL"],
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_db() -> t.Generator[Session, None, None]:
    db: t.Optional[Session] = None
    try:
        logging.debug("Getting database session connection ...")
        db = SessionLocal()
        logging.debug("Successfully retrieved database session connection")
        yield db
    finally:
        if db:
            logging.debug("Closing database session connection ...")
            db.close()
            logging.debug("Successfully closed database session connection")


BaseModel = declarative_base()
