import typing as t

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from database.orm import get_db
from main import api


@pytest.fixture(scope="function")
def db() -> Session:
    yield next(get_db())


@pytest.fixture()
def test_client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:
    """
    with TestClient(app=api) as _test_client:
        yield _test_client
