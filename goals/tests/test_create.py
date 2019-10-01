from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from goals.models import Goal


class TestGoalsCreate(TestCase):
    def setUp(self):
        self.url = reverse('api:goals-create-list')

    def test_url(self):
        self.assertEqual(self.url, '/v1/goals/')

    def test_create_valid(self):
        count_before = Goal.objects.all().count()

        with freeze_time('1970-01-01T12:34:56'):
            response = self.client.post(
                self.url,
                {
                    'text': 'some-text'
                }
            )

        count_after = Goal.objects.all().count()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'created': '1970-01-01T12:34:56',
                'id': str(Goal.objects.latest('created').id),
                'text': 'some-text',
            },
        )
        self.assertEqual(count_after, count_before + 1)
