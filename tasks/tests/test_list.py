from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from goals.models import Goal
from tasks.models import Task


class TestTasksList(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_url(self):
        self.assertEqual(reverse('api:tasks-create-list'), '/v1/tasks/')

    def test_list_in_correct_order(self):
        goal_id = Goal.objects.create().id
        with freeze_time('1970-01-01T12:34:51'):
            task_first = Task.objects.create(parent_id=goal_id)
        with freeze_time('1970-01-01T12:34:52'):
            task_second = Task.objects.create(parent_id=goal_id)
        with freeze_time('1970-01-01T12:34:53'):
            task_third = Task.objects.create(parent_id=goal_id)

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
                        'parent_id': str(goal_id),
                    },
                    {
                        'id': str(task_second.id),
                        'created': '1970-01-01T12:34:52',
                        'parent_id': str(goal_id),
                    },
                    {
                        'id': str(task_first.id),
                        'created': '1970-01-01T12:34:51',
                        'parent_id': str(goal_id),
                    },
                ],
            },
        )
