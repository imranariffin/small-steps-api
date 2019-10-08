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

    def test_get_parent_goal(self):
        goal = Goal.objects.create()
        task = Task.objects.create(parent_id=goal.id, text='some-text-0')

        parent = task.get_parent()

        self.assertEqual(parent, goal)

    def test_get_parent_task(self):
        goal_id = Goal.objects.create().id
        task_parent = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        )
        task = Task.objects.create(
            parent_id=task_parent.id,
            text='some-text-1',
        )

        parent = task.get_parent()

        self.assertEqual(parent, task_parent)

    def test_get_siblings_in_descending_created_order(self):
        goal_id = Goal.objects.create().id
        task_parent = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        )
        task = Task.objects.create(
            parent_id=task_parent.id,
            text='some-text-1',
        )
        task_sibling_first = Task.objects.create(
            parent_id=task_parent.id,
            text='some-text-2',
        )
        task_sibling_second = Task.objects.create(
            parent_id=task_parent.id,
            text='some-text-3',
        )

        siblings = list(task.get_siblings())

        self.assertEqual(len(siblings), 2)
        self.assertEqual(siblings[0], task_sibling_second)
        self.assertEqual(siblings[1], task_sibling_first)

    def test_get_subtasks_in_descending_created_order(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        )
        task_subtask_first = Task.objects.create(
            parent_id=task.id,
            text='some-text-1',
        )
        task_subtask_second = Task.objects.create(
            parent_id=task.id,
            text='some-text-2',
        )
        task_subtask_third = Task.objects.create(
            parent_id=task.id,
            text='some-text-3',
        )

        subtasks = list(task.get_subtasks())

        self.assertEqual(len(subtasks), 3)
        self.assertEqual(subtasks[0], task_subtask_third)
        self.assertEqual(subtasks[1], task_subtask_second)
        self.assertEqual(subtasks[2], task_subtask_first)
