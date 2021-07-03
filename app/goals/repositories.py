import typing as t

from app.goals.models import Goal


class GoalsRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self) -> t.List[Goal]:
        return self.db.query(Goal).all()
