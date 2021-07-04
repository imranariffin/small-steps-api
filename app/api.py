from os import environ
from typing import Dict, List, Optional

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
    def get_base_url() -> str:
        return f"http://{environ['API_HOST']}:{environ['API_PORT']}"

    def get_routes_map(routes: List) -> Dict[str, str]:
        return {
            route.name: f"{get_base_url()}{route.path}"
            for route in routes
        }

    return get_routes_map(api.routes)


@api.get("/goals", response_model=List[GoalsResponse])
def get_all_goals(db: Session = Depends(get_db)):
    return [
        GoalsResponse(id=g.id, title=g.title)
        for g in GoalsRepository(db=db).get_all()
    ]
