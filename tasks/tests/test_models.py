from django.db.utils import IntegrityError
from django.test import TestCase

from goals.models import Goal
from tasks.models import Task
from tasks.exceptions import ParentDoesNotExist


class TestTaskModel(TestCase):
    def test_create_valid(self):
        goal_id = Goal.objects.create().id
        count_before = Task.objects.all().count()

        Task.objects.create(parent_id=goal_id, text='some-text')

        count_after = Task.objects.all().count()
        self.assertEqual(count_after, count_before + 1)

    def test_parent_missing(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(text='some-text')

    def test_text_missing(self):
        goal_id = Goal.objects.create().id

        with self.assertRaises(IntegrityError):
            Task.objects.create(parent_id=goal_id)

    def test_parent_goal_does_not_exist(self):
        goal_id = Goal.objects.create().id
        Goal.objects.all().delete()
        count_before = Task.objects.all().count()

        with self.assertRaises(ParentDoesNotExist):
            Task.objects.create(parent_id=goal_id)

        count_after = Task.objects.all().count()
        self.assertEqual(count_after, count_before)

    def test_parent_task_does_not_exist(self):
        goal_id = Goal.objects.create().id
        task_id = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        ).id
        Task.objects.all().delete()
        count_before = Task.objects.all().count()

        with self.assertRaises(ParentDoesNotExist):
            Task.objects.create(parent_id=task_id, text='some-text-1')

        count_after = Task.objects.all().count()
        self.assertEqual(count_after, count_before)

    def test_initial_status(self):
        goal_id = Goal.objects.create().id

        task = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        )

        self.assertEqual(task.status, 'not_started')
