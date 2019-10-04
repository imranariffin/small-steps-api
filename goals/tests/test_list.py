from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from goals.models import Goal


class TestGoalsList(TestCase):
    def setUp(self):
        Goal.objects.all().delete()

    def test_existing_goals_in_correct_order(self):
        with freeze_time('1970-01-01T12:34:56'):
            goal_first = Goal.objects.create(text='goal-first-text')
        with freeze_time('1970-01-01T12:34:55'):
            goal_second = Goal.objects.create(text='goal-second-text')

        response = self.client.get(reverse('api:goals-create-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'goals': [
                    {
                        'created': '1970-01-01T12:34:56',
                        'id': str(goal_first.id),
                        'text': 'goal-first-text'
                    },
                    {
                        'created': '1970-01-01T12:34:55',
                        'id': str(goal_second.id),
                        'text': 'goal-second-text'
                    }
                ]
            }
        )
