from django.test import TestCase, tag
from common.models import People
from django.contrib.auth import get_user_model


@tag('models', 'people')
class PeopleCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get_or_create(username="test", password="test")[0]

    def test_create(self):
        obj = People.objects.create(name="test", creator=self.user)
        self.assertIsNotNone(obj.id)
