from sqlalchemy import Column, Integer, String

from app.database.orm import BaseModel


class Goal(BaseModel):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
