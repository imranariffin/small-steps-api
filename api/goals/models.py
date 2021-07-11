from sqlalchemy import Column, Integer, String

from database.orm import BaseModel


class Goal(BaseModel):
    __tablename__ = "goals"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)
