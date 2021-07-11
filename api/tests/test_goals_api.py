
import pytest

from sqlalchemy.orm import Session

from goals.models import Goal


@pytest.fixture()
def goal_1(db: Session):
    goal: Goal = Goal(title="Goal 1")
    db.add(goal)
    db.commit()
    db.refresh(goal)
    yield goal
    db.delete(goal)
    db.commit()


@pytest.fixture()
def goal_2(db: Session):
    goal: Goal = Goal(title="Goal 2")
    db.add(goal)
    db.commit()
    db.refresh(goal)
    yield goal
    db.delete(goal)
    db.commit()


def test_get_all_goals__empty(test_client):
    # Given no existing goals
    # When a request has been made to list all goals
    response = test_client.get("/goals")

    # Then the request should be successful
    assert response.status_code == 200, response
    # And the response should be empty
    assert response.json() == []


def test_get_all_goals__some_existing(test_client, goal_1: Goal, goal_2: Goal):
    # Given some existing goals goal_1 and goal_2
    # When a request has been made to list all goals
    response = test_client.get("/goals")

    # Then the request should be successful
    assert response.status_code == 200, response
    # And the response lists all existing goals in correct order
    assert response.json() == [
        {
            "id": goal_1.id,
            "title": goal_1.title,
        },
        {
            "id": goal_2.id,
            "title": goal_2.title,
        },
    ]


def test_create_goal__success(db, test_client):
    # When a valid request has been made to create a new goal
    response = test_client.post("/goals/", json={"title": "Some new goal"})

    # Then the request should be successful
    assert response.status_code == 200, response
    # And the goal should be saved in db
    created_goal = db.query(Goal).filter(Goal.title == "Some new goal").first()
    assert created_goal is not None
    # And the response should be correct
    assert response.json() == {
        "id": created_goal.id,
        "title": "Some new goal",
    }

    db.delete(created_goal)
    db.commit()


def test_retrieve_existing_goal__success(db, test_client, goal_1):
    # When a valid request has been made to retreive an existing goal
    response = test_client.get(f"/goals/{goal_1.id}/")

    # Then the request should be successful
    assert response.status_code == 200, response
    # And the response should be correct
    assert response.json() == {
        "id": goal_1.id,
        "title": goal_1.title,
    }


def test_retrieve_non_existing_goal__fail(db, test_client, goal_1):
    # When a valid request has been made to retrieve a non-existing goal
    response = test_client.get(f"/goals/999/")

    # Then the request should fail
    assert response.status_code == 404, response
    # And the response should contain an appropriate error message
    assert response.json() == {
        "detail": "Goal with id=999 does not exist",
    }
