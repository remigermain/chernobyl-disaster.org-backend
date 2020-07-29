from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from lib.utils import contenttypes_uuid
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

ISO_8601 = 'iso-8601'


class BaseTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username='username',
            email='email@email.email',
            password='password'
            )
        self.request = RequestFactory
        self.request.user = self.user
        self.context = {
            'request': self.request
        }
        self.lang = settings.LANGUAGES_DEFAULT
        self.langs = [lang[0] for lang in settings.LANGUAGES]
        self.lang2 = [lang for lang in self.langs if lang is not self.lang][0]
        self.lang_wrong = 'wrong'
        self.time = timezone.now()
        self.link = 'https://chernobyl.org'
        self.link2 = 'https://chernobyl.com'
        self.link_wrong = 'wrong link'

    def delta_time(self, **kwargs):
        return self.time - timezone.timedelta(**kwargs)

    def str_to_time(self, date):
        return parse_datetime(date)

    def check_creator(self, obj, user=None):
        user = user or self.user
        self.assertEqual(obj.creator, user)
        self.assertIsNotNone(obj.created)

    def check_commit(self, obj, user=None):
        from common.models import Commit
        user = user or self.user
        commit = Commit.objects.filter(uuid=contenttypes_uuid(Commit, obj))
        self.assertEqual(commit.count(), 1)
        commit = commit.first()
        self.assertEqual(commit.creator, user)
        self.assertIsNotNone(commit.created)

    def check_update_language(self, obj, old_language, new_language):
        self.assertNotEqual(obj.language, old_language)
        self.assertEqual(obj.language, new_language)
