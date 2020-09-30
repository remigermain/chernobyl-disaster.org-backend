from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from utils.function import contenttypes_uuid
from django.conf import settings
from django.utils import timezone, datetime_safe
from utils.models import Commit
from rest_framework.test import APIClient

class BaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.username = 'username'
        cls.email = 'email@email.email'
        cls.password = 'ER5dd[]433-444e'

        cls.user = get_user_model().objects.create(
            username=cls.username,
            email=cls.email,
            is_active=True
        )
        cls.user.set_password(cls.password)

        cls.user_admin = get_user_model().objects.create(
            username=f"admin{cls.username}",
            email=f"admin{cls.email}",
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        cls.user_admin.set_password(cls.password)

        cls.request = RequestFactory
        cls.request.user = cls.user
        cls.context = {'request': cls.request}

        cls.lang = settings.LANGUAGES_DEFAULT
        langs = [lang[0] for lang in settings.LANGUAGES]
        cls.lang2 = [lang for lang in langs if lang is not cls.lang][0]
        cls.time = timezone.now()
        cls.time2 = timezone.now() - timezone.timedelta(days=9)

        cls.date = datetime_safe.new_date(cls.time)
        cls.date2 = datetime_safe.new_date(cls.time2)

        cls.factory = APIClient()
        cls.factory.force_authenticate(user=cls.user)
        cls.factory_admin = APIClient()
        cls.factory_admin.force_authenticate(user=cls.user_admin)

    def get_anonymous_user(self):
        self.context['request'].user = AnonymousUser()
        return self.context

    def check_creator(self, obj, user=None):
        user = user or self.user
        self.assertEqual(obj.creator, user)
        self.assertIsNotNone(obj.created)

    def check_commit(self, obj, created=True):
        commit = Commit.objects.filter(uuid=contenttypes_uuid(obj), created=created)
        self.assertEqual(commit.count(), 1)
        commit = commit.first()
        self.assertEqual(commit.creator, self.user)
        self.assertEqual(commit.created, created)

    def check_commit_created(self, instance, creator=None):
        if not creator:
            creator = self.user
        uuid = contenttypes_uuid(instance)
        query = Commit.objects.filter(uuid=uuid)
        self.assertEqual(query.count(), 1)
        commit = query.first()
        self.assertEqual(commit.creator, creator)
        self.assertIsNone(commit.updated_fields)
        self.assertTrue(commit.created)

    def check_not_commit_created(self, instance):
        query = Commit.objects.filter(uuid=contenttypes_uuid(instance))
        self.assertEqual(query.count(), 0)

    def check_commit_update(self, instance, diff, creator=None):
        if not creator:
            creator = self.user
        uuid = contenttypes_uuid(instance)
        query = Commit.objects.filter(uuid=uuid, created=False)
        self.assertEqual(query.count(), 1)
        commit = query.first()
        self.assertEqual(commit.creator, creator)
        self.assertSetEqual(set(commit.updated_fields.split("|")), set(diff))
