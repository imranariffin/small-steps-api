from typing import Optional

from pydantic import BaseModel


class GoalsResponse(BaseModel):
    id: int
    title: Optional[str] = None

    class Config:
        orm_mode = True


class GoalsErrorResponse(BaseModel):
    message: str


class GoalCreateRequest(BaseModel):
    title: Optional[str] = None
