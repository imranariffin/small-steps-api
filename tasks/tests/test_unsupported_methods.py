from django.test import TestCase
from django.utils import dateparse

from tasks.models import Task
from goals.models import Goal


class TestGoalsUnsupportedMethods(TestCase):
    def setUp(self):
        Task.objects.all().delete()

    def test_retrieve(self):
        goal_existing = Goal.objects.create()
        task_existing_id = Task.objects.create(
            parent_id=goal_existing.id,
            text='some-text',
        ).id

        response = self.client.get(f'v1/tasks/{task_existing_id}')

        self.assertEqual(response.status_code, 404)

    def test_update(self):
        goal_existing = Goal.objects.create()
        task_existing = Task.objects.create(
            created='1970-01-01T12:34:56',
            text='some-original-text',
            parent_id=goal_existing.id,
        )

        response = self.client.patch(f'v1/tasks/{task_existing.id}')

        task_existing.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(task_existing.text, 'some-original-text')
        self.assertEqual(
            task_existing.created,
            dateparse.parse_datetime('1970-01-01T12:34:56'),
        )

    def test_delete(self):
        goal_existing = Goal.objects.create()
        task_existing = Task.objects.create(
            created='1970-01-01T12:34:56',
            text='some-original-text',
            parent_id=goal_existing.id,
        )

        response = self.client.delete(f'v1/tasks/{task_existing.id}')

        task_existing.refresh_from_db()
        self.assertEqual(response.status_code, 404)
