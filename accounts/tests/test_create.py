from django.test import TestCase
from django.urls import reverse


class TestAccountsCreate(TestCase):
    def test_url(self):
        self.assertEqual(reverse('api:accounts-create'), '/v1/accounts/')

    def test_create(self):
        url = reverse('api:accounts-create')

        response = self.client.post(
            url,
            {
                'device_id': 'some-device-id',
            }
        )

        self.assertEqual(response.status_code, 201)
