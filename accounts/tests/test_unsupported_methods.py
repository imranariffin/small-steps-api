from django.test import TestCase
from django.utils import dateparse

from accounts.models import Account


class TestAccountsUnsupportedMethods(TestCase):
    def setUp(self):
        Account.objects.all().delete()

    def test_list(self):
        response = self.client.get(f'/v1/accounts/')

        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        account_existing_id = Account.objects.create().id

        response = self.client.delete(f'/v1/accounts/{account_existing_id}/')

        self.assertEqual(response.status_code, 404)

    def test_retrieve(self):
        account_existing_id = Account.objects.create().id

        response = self.client.get(f'/v1/accounts/{account_existing_id}/')

        self.assertEqual(response.status_code, 404)

    def test_update(self):
        account_existing = Account.objects.create(
            created='1970-01-01T12:34:56',
            device_id='some-device-id',
        )

        response = self.client.patch(f'/v1/accounts/{account_existing.id}/')

        account_existing.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(account_existing.device_id, 'some-device-id')
        self.assertEqual(
            account_existing.created,
            dateparse.parse_datetime('1970-01-01T12:34:56'),
        )
