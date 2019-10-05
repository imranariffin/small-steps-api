from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from tasks.models import Task


class TestCreateTasks(TestCase):
    def test_url(self):
        self.assertEqual(reverse('api:tasks-create'), '/v1/tasks/')

    def test_create_valid(self):
        count_before = Task.objects.count()

        with freeze_time('1970-01-01T12:34:56'):
            response = self.client.post(
                reverse('api:tasks-create'),
                {
                    'parent_id': 'some-existing-goal-id',
                    'text': 'some-tasks-text',
                },
                content_type='application/json',
            )

        count_after = Task.objects.count()
        task_id = response.data['id']
        task = Task.objects.get(id=task_id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'created': '1970-01-01T12:34:56',
                'id': str(task_id),
                'parent_id': 'some-existing-goal-id',
                'text': 'some-tasks-text',
            }
        )
        self.assertEqual(count_after, count_before + 1)
