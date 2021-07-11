from typing import List

from fastapi import Depends, Path, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from database.orm import get_db
from goals.api_schemas import GoalCreateRequest, GoalsResponse
from goals.repositories import GoalsRepository

router = APIRouter()


@router.get("/", response_model=List[GoalsResponse])
def get_all_goals(db: Session = Depends(get_db)):
    all_goals = GoalsRepository(db=db).get_all()
    return all_goals


@router.post("/", response_model=GoalsResponse)
def create_goal(goal_create: GoalCreateRequest, db: Session = Depends(get_db)):
    goal = GoalsRepository(db=db).create(goal_create=goal_create)
    return goal


@router.get("/{goal_id}", response_model=GoalsResponse)
def retrieve_goal(
    goal_id: int = Path(default=None, title="Goal ID to query by"),
    db: Session = Depends(get_db),
):
    goal = GoalsRepository(db=db).get_by_id(id=goal_id)
    if goal is None:
        raise HTTPException(
            status_code=404,
            detail=f"Goal with id={goal_id} does not exist",
        )
    return goal
