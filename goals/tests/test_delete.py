import uuid

from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from goals.models import Goal


class TestGoalsDelete(TestCase):
    def test_url(self):
        goal_id = Goal.objects.create(text='some-existing-goal-0').id
        self.assertEqual(
            reverse('api:goals-delete', args=[goal_id]),
            f'/v1/goals/{goal_id}/',
        )

    def test_delete_existing(self):
        goal_existing_id = Goal.objects.create(text='some-existing-goal-1').id
        url = reverse('api:goals-delete', args=[goal_existing_id])
        count_before = Goal.objects.filter(goaldeleted__isnull=True).count()

        with freeze_time('1970-01-01T12:34:56'):
            response = self.client.delete(url)

        count_after = Goal.objects.filter(goaldeleted__isnull=True).count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'datetime_deleted': '1970-01-01T12:34:56',
                'id': str(goal_existing_id),
            }
        )
        self.assertEqual(count_after, count_before - 1)

    def test_delete_nonexisting(self):
        goal_nonexisting_id = uuid.uuid4()
        url = reverse('api:goals-delete', args=[goal_nonexisting_id])
        count_before = Goal.objects.all().count()

        response = self.client.delete(url)

        count_after = Goal.objects.all().count()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                'goal_id': f'Goal with id {goal_nonexisting_id} not found',
            }
        )
        self.assertEqual(count_after, count_before)
