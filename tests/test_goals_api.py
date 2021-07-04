from fastapi.testclient import TestClient

from app.api import api


test_client = TestClient(app=api)


def test_get_all_goals__empty():
    response = test_client.get("/goals")

    assert response.status_code == 200, response
    assert response.json() == []
