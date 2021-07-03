from typing import List, Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.orm import get_db
from app.goals.repositories import GoalsRepository


api = FastAPI()


class GoalsResponse(BaseModel):
    id: int
    title: Optional[str] = None


@api.get("/")
def root():
    return {}


@api.get("/goals", response_model=List[GoalsResponse])
def get_all_goals(db: Session = Depends(get_db)):
    return [
        GoalsResponse(id=g.id, title=g.title)
        for g in GoalsRepository(db=db).get_all()
    ]
