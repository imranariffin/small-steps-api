from django.test import TestCase

from goals.models import Goal, GoalDeleted


class TestGoalModel(TestCase):
    def test_mark_delete(self):
        goal = Goal.objects.create(text='some-goal-text')

        goal.delete()

        goal.refresh_from_db()
        self.assertEqual(Goal.objects.get(id=goal.id), goal)
        self.assertEqual(goal.id, GoalDeleted.objects.get(goal=goal).goal.id)
