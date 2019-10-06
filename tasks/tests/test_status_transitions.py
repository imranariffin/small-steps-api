from django.test import TestCase

from goals.models import Goal
from tasks.models import Task


class TestStatusTransitions(TestCase):
    def test_transition_to_completed_with_no_subtask(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            status='in_progress',
            text='some-text-0',
        )

        task.transition_to('completed')

        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')

    def test_transition_to_in_progress_with_no_subtask(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            status='not_started',
            text='some-text-0',
        )

        task.transition_to('in_progress')

        task.refresh_from_db()
        self.assertEqual(task.status, 'in_progress')

    def test_transition_to_completed_with_subtasks(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            status='in_progress',
            text='some-text-0',
        )
        subtask_first = Task.objects.create(
            parent_id=task.id,
            status='in_progress',
            text='some-text-1',
        )
        subtask_second = Task.objects.create(
            parent_id=task.id,
            status='not_started',
            text='some-text-2',
        )

        task.transition_to('completed')

        task.refresh_from_db()
        subtask_first.refresh_from_db()
        subtask_second.refresh_from_db()
        self.assertEqual(task.status, 'completed')
        self.assertEqual(subtask_first.status, 'completed')
        self.assertEqual(subtask_second.status, 'completed')

    def test_transition_to_completed_with_task_parent(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            status='in_progress',
            text='some-text-0',
        )
        subtask = Task.objects.create(
            parent_id=task.id,
            status='in_progress',
            text='some-text-1',
        )

        subtask.transition_to('completed')

        subtask.refresh_from_db()
        task.refresh_from_db()
        self.assertEqual(subtask.status, 'completed')
        self.assertEqual(task.status, 'in_progress')

    def test_transition_to_completed_with_descendant_subtasks(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            status='in_progress',
            text='some-text-0',
        )
        subtask = Task.objects.create(
            parent_id=task.id,
            status='in_progress',
            text='some-text-1',
        )
        subsubtask_first = Task.objects.create(
            parent_id=task.id,
            status='not_started',
            text='some-text-2',
        )
        subsubtask_second = Task.objects.create(
            parent_id=task.id,
            status='in_progress',
            text='some-text-3',
        )

        task.transition_to('completed')

        task.refresh_from_db()
        subtask.refresh_from_db()
        subsubtask_first.refresh_from_db()
        subsubtask_second.refresh_from_db()
        self.assertEqual(task.status, 'completed')
        self.assertEqual(subtask.status, 'completed')
        self.assertEqual(subsubtask_first.status, 'completed')
        self.assertEqual(subsubtask_second.status, 'completed')

    def test_transition_to_in_progress_with_subtasks(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            status='not_started',
            text='some-text-0',
        )
        subtask_first = Task.objects.create(
            parent_id=task.id,
            status='not_started',
            text='some-text-1',
        )
        subtask_second = Task.objects.create(
            parent_id=task.id,
            status='not_started',
            text='some-text-2',
        )

        task.transition_to('in_progress')

        task.refresh_from_db()
        subtask_first.refresh_from_db()
        subtask_second.refresh_from_db()
        self.assertEqual(task.status, 'in_progress')
        self.assertEqual(subtask_first.status, 'in_progress')
        self.assertEqual(subtask_second.status, 'in_progress')