from django.test import TestCase
from django.urls import reverse

from goals.models import Goal
from tasks.models import Task


class TestStatusUpdate(TestCase):
    def test_url(self):
        goal_id = Goal.objects.create().id
        task_id = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        ).id

        self.assertEqual(
            reverse('api:tasks-status-update', args=[task_id]),
            f'/v1/tasks/{task_id}/status/',
        )

    def test_from_not_started_to_not_started(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        )
        status_before = task.status

        response = self.client.put(
            reverse('api:tasks-status-update', args=[task.id]),
            {
                'status': 'not_started',
            },
            content_type='application/json',
        )

        task.refresh_from_db()
        status_after = task.status
        self.assertEqual(response.status_code, 200)
        self.assertEqual(status_after, status_before)

    def test_from_not_started_to_in_progress(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            text='some-text-0',
        )

        response = self.client.put(
            reverse('api:tasks-status-update', args=[task.id]),
            {
                'status': 'in_progress',
            },
            content_type='application/json',
        )

        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.status, 'in_progress')
        self.assertEqual(
            response.json(),
            {
                'id': str(task.id),
                'status': 'in_progress',
            }
        )

    def test_from_in_progress_to_completed(self):
        goal_id = Goal.objects.create().id
        task = Task.objects.create(
            parent_id=goal_id,
            status='in_progress',
            text='some-text-0',
        )

        response = self.client.put(
            reverse('api:tasks-status-update', args=[task.id]),
            {
                'status': 'completed',
            },
            content_type='application/json',
        )

        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.status, 'completed')
        self.assertEqual(
            response.json(),
            {
                'id': str(task.id),
                'status': 'completed',
            }
        )

    def test_unrecognized_status(self):
        for status_before in ['not_started', 'in_progress', 'completed']:
            goal_id = Goal.objects.create().id
            task = Task.objects.create(
                parent_id=goal_id,
                status=status_before,
                text='some-text-0',
            )

            response = self.client.put(
                reverse('api:tasks-status-update', args=[task.id]),
                {
                    'status': 'some_unrecognized_status',
                },
                content_type='application/json',
            )

            task.refresh_from_db()
            self.assertEqual(response.status_code, 400)
            self.assertEqual(task.status, status_before)
            self.assertEqual(
                response.json(),
                {
                    'status': f'Status some_unrecognized_status is not valid',
                }
            )
