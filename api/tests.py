from django.test import TestCase
from django.urls import reverse


class TestGoalsCreate(TestCase):
    def setUp(self):
        self.url = reverse('api:goals-create')

    def test_url(self):
        self.assertEqual(self.url, '/v1/goals/')

    def test_create(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 201)
