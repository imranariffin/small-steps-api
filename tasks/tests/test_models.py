from django.db.utils import IntegrityError
from django.test import TestCase

from tasks.models import Task
from goals.models import Goal


class TestTaskModel(TestCase):
    def test_create_valid(self):
        goal_id = Goal.objects.create().id
        count_before = Task.objects.all().count()

        Task.objects.create(parent_id=goal_id)

        count_after = Task.objects.all().count()
        self.assertEqual(count_after, count_before + 1)
    
    def test_parent_empty(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create()
    
    def test_parent_goal_does_not_exist(self):
        goal_id = Goal.objects.create().id
        Goal.objects.all().delete()
        count_before = Task.objects.all().count()

        with self.assertRaises(IntegrityError):
            Task.objects.create(parent_id=goal_id)

        count_after = Task.objects.all().count()
        self.assertEqual(count_after, count_before)

    def test_parent_task_does_not_exist(self):
        goal_id = Goal.objects.create().id
        task_id = Task.objects.create(parent_id=goal_id).id
        Task.objects.all().delete()
        count_before = Task.objects.all().count()

        with self.assertRaises(IntegrityError):
            Task.objects.create(parent_id=task_id)

        count_after = Task.objects.all().count()
        self.assertEqual(count_after, count_before)
