from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from utils.function import contenttypes_uuid
from django.conf import settings
from django.utils import timezone, datetime_safe
from django.utils.dateparse import parse_datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from utils.models import Commit
from rest_framework.test import force_authenticate, APIClient

ISO_8601 = 'iso-8601'


class BaseTest(TestCase):

    def setUp(self):
        self.username = 'username'
        self.email = 'email@email.email'
        self.password = 'password'
        self.user = get_user_model().objects.create(
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=True
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
        self.time2 = timezone.now() - timezone.timedelta(days=9)

        self.date = datetime_safe.new_date(self.time)
        self.date2 = datetime_safe.new_date(self.time2)
        self.link = 'https://chernobyl.org'
        self.link2 = 'https://chernobyl.com'
        self.link_wrong = 'wrong link'
        self.reverse = reverse

        self.image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.document = SimpleUploadedFile('small.gif', self.image, content_type='image/gif')
        self.document2 = SimpleUploadedFile('small2.gif', self.image, content_type='image/gif')
        self.picture = self.document
        self.picture2 = self.document2
        
        self.factory = APIClient()
        self.factory.force_authenticate(user=self.user)
    
    def get_user(self):
        return get_user_model().objects.get(
            username=self.username,
            email=self.email,
            password=self.password,
        )

    def get_anonymous_user(self):
        self.context['request'].user = AnonymousUser()
        return self.context

    def delta_time(self, **kwargs):
        return self.time - timezone.timedelta(**kwargs)

    def str_to_time(self, date):
        return parse_datetime(date)

    def check_creator(self, obj, user=None):
        # user = user or self.user
        # self.assertEqual(obj.creator, user)
        # self.assertIsNotNone(obj.created)
        pass

    def check_commit(self, obj, created=True):
        commit = Commit.objects.filter(uuid=contenttypes_uuid(obj), created=created)
        self.assertEqual(commit.count(), 1)
        commit = commit.first()
        self.assertEqual(commit.creator, self.user)
        self.assertEqual(commit.created, created)

    def check_update_language(self, obj, old_language, new_language):
        self.assertNotEqual(obj.language, old_language)
        self.assertEqual(obj.language, new_language)



    def check_commit_created(self, instance, creator=None):
        if not creator:
            creator = self.user
        uuid = contenttypes_uuid(instance)
        query = Commit.objects.filter(uuid=uuid)
        self.assertEqual(query.count(), 1)
        commit = query.first()
        self.assertEqual(commit.creator, creator)
        self.assertIsNone(commit.updated_field)
        self.assertTrue(commit.created)

    def check_commit_update(self, instance, diff, creator=None):
        if not creator:
            creator = self.user
        uuid = contenttypes_uuid(instance)
        query = Commit.objects.filter(uuid=uuid, created=False)
        self.assertEqual(query.count(), 1)
        commit = query.first()
        self.assertEqual(commit.creator, creator)
        self.assertEqual(commit.updated_field.split("|"), diff)
