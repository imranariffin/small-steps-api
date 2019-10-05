from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from tasks.models import Task


class TestTasksList(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_url(self):
        self.assertEqual(reverse('api:tasks-create-list'), '/v1/tasks/')

    def test_list_in_correct_order(self):
        with freeze_time('1970-01-01T12:34:51'):
            task_first = Task.objects.create()
        with freeze_time('1970-01-01T12:34:52'):
            task_second = Task.objects.create()
        with freeze_time('1970-01-01T12:34:53'):
            task_third = Task.objects.create()

        response = self.client.get(
            reverse('api:tasks-create-list'),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'tasks': [
                    {
                        'id': str(task_third.id),
                        'created': '1970-01-01T12:34:53',
                    },
                    {
                        'id': str(task_second.id),
                        'created': '1970-01-01T12:34:52',
                    },
                    {
                        'id': str(task_first.id),
                        'created': '1970-01-01T12:34:51',
                    },
                ],
            },
        )
