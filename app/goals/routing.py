from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.database.orm import get_db
from app.goals.api_schemas import GoalCreateRequest, GoalsResponse
from app.goals.repositories import GoalsRepository

router = APIRouter()


@router.get("/", response_model=List[GoalsResponse])
def get_all_goals(db: Session = Depends(get_db)):
    all_goals = GoalsRepository(db=db).get_all()
    return all_goals


@router.post("/", response_model=GoalsResponse)
def create_goal(goal_create: GoalCreateRequest, db: Session = Depends(get_db)):
    goal = GoalsRepository(db=db).create(goal_create=goal_create)
    return goal
