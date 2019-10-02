from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from accounts.models import Account


class TestAccountsCreate(TestCase):
    def test_url(self):
        self.assertEqual(reverse('api:accounts-create'), '/v1/accounts/')

    def test_valid(self):
        url = reverse('api:accounts-create')

        with freeze_time('1970-01-01T12:34:56'):
            response = self.client.post(
                url,
                {
                    'device_id': 'some-device-id',
                }
            )

        account_id = Account.objects.get(device_id='some-device-id').id
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id': str(account_id),
                'created': '1970-01-01T12:34:56',
            }
        )

    def test_existing_device_id(self):
        url = reverse('api:accounts-create')
        Account.objects.create(device_id='some-existing-device-id')

        with freeze_time('1970-01-01T12:34:56'):
            response = self.client.post(
                url,
                {
                    'device_id': 'some-existing-device-id',
                }
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'device_id': (
                    'Device id some-existing-device-id '
                    'already exists'
                ),
            }
        )
