from django.test import tag
from lib.test import BaseTest
from django.urls import reverse


@tag('event')
class PopulateTest(BaseTest):

    @tag('auth')
    def test_auth(self):
        response = self.client.get(reverse('populate_store'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('populate_picture'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('populate_people'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('populate_overview'))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse('populate_contributors'))
        self.assertEqual(response.status_code, 403)

    def test_store(self):
        response = self.factory.get(reverse('populate_store'))
        self.assertEqual(response.status_code, 200)

    def test_picture(self):
        response = self.factory.get(reverse('populate_picture'))
        self.assertEqual(response.status_code, 200)

    def test_people(self):
        response = self.factory.get(reverse('populate_people'))
        self.assertEqual(response.status_code, 200)

    def test_overview(self):
        response = self.factory.get(reverse('populate_overview'))
        self.assertEqual(response.status_code, 200)

    def test_contributors(self):
        response = self.factory.get(reverse('populate_contributors'))
        self.assertEqual(response.status_code, 200)
