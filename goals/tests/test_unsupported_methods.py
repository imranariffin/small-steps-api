from django.test import TestCase
from django.urls import reverse
from django.utils import dateparse

from goals.models import Goal


class TestGoalsUnsupportedMethods(TestCase):
    def setUp(self):
        Goal.objects.all().delete()

    def test_list(self):
        response = self.client.get(reverse('api:goals-create'))

        self.assertEqual(response.status_code, 405)

    def test_retrieve(self):
        goal_existing_id = Goal.objects.create().id

        response = self.client.get(f'v1/goals/{goal_existing_id}')

        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        goal_existing_id = Goal.objects.create().id

        response = self.client.delete(f'v1/goals/{goal_existing_id}')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Goal.objects.all().count(), 1)

    def test_update(self):
        goal_existing = Goal.objects.create(
            text='some-original-text',
            created='1970-01-01T12:34:56',
        )

        response = self.client.patch(f'v1/goals/{goal_existing.id}')

        goal_existing.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(goal_existing.text, 'some-original-text')
        self.assertEqual(
            goal_existing.created,
            dateparse.parse_datetime('1970-01-01T12:34:56'),
        )
