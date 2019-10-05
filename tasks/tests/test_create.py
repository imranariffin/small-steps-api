import uuid

from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from tasks.models import Task
from goals.models import Goal


class TestCreateTasks(TestCase):
    def test_url(self):
        self.assertEqual(reverse('api:tasks-create'), '/v1/tasks/')

    def test_create_valid_goal_parent(self):
        goal_existing_id = Goal.objects.create(text='some-parent-text').id
        count_before = Task.objects.count()

        with freeze_time('1970-01-01T12:34:56'):
            response = self.client.post(
                reverse('api:tasks-create'),
                {
                    'parent_id': goal_existing_id,
                    'text': 'some-tasks-text',
                },
                content_type='application/json',
            )

        count_after = Task.objects.count()
        self.assertEqual(response.status_code, 201)
        task_id = response.data['id']
        self.assertEqual(
            response.json(),
            {
                'created': '1970-01-01T12:34:56',
                'id': str(task_id),
                'parent_id': str(goal_existing_id),
                'text': 'some-tasks-text',
            }
        )
        self.assertEqual(count_after, count_before + 1)

    def test_create_valid_task_parent(self):
        task_existing_id = Task.objects.create().id
        count_before = Task.objects.count()

        with freeze_time('1970-01-01T12:34:56'):
            response = self.client.post(
                reverse('api:tasks-create'),
                {
                    'parent_id': task_existing_id,
                    'text': 'some-tasks-text',
                },
                content_type='application/json',
            )

        self.assertEqual(response.status_code, 201)
        count_after = Task.objects.count()
        task_id = response.data['id']
        self.assertEqual(
            response.json(),
            {
                'created': '1970-01-01T12:34:56',
                'id': str(task_id),
                'parent_id': str(task_existing_id),
                'text': 'some-tasks-text',
            }
        )
        self.assertEqual(count_after, count_before + 1)

    def test_create_missing_text(self):
        count_before = Task.objects.count()
        goal_existing_id = Goal.objects.create(text='some-goal-text').id

        response = self.client.post(
            reverse('api:tasks-create'),
            {
                'parent_id': goal_existing_id,
            },
            content_type='application/json',
        )

        count_after = Task.objects.count()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'text': 'This field is required',
            },
        )
        self.assertEqual(count_after, count_before)

    def test_create_missing_parent_id(self):
        count_before = Task.objects.count()
        Goal.objects.create(text='some-goal-text')

        response = self.client.post(
            reverse('api:tasks-create'),
            {
                'text': 'some-tasks-text',
            },
            content_type='application/json',
        )

        count_after = Task.objects.count()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'parent_id': 'This field is required',
            },
        )
        self.assertEqual(count_after, count_before)

    def test_create_parent_not_found(self):
        parent_id = uuid.uuid4()
        count_before = Task.objects.count()

        response = self.client.post(
            reverse('api:tasks-create'),
            {
                'text': 'some-tasks-text',
                'parent_id': parent_id,
            },
            content_type='application/json',
        )

        count_after = Task.objects.count()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'parent_id': (
                    f'Parent with id {parent_id} does not exist'
                ),
            },
        )
        self.assertEqual(count_after, count_before)
