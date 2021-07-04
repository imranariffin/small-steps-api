import typing as t

from sqlalchemy.orm import Session

from app.goals.api_schemas import GoalCreateRequest
from app.goals.models import Goal


class GoalsRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_all(self) -> t.List[Goal]:
        return self.db.query(Goal).all()

    def create(self, *, goal_create: GoalCreateRequest) -> Goal:
        goal: Goal = Goal(**goal_create.dict())
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal
