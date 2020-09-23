from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from utils.function import contenttypes_uuid
from django.conf import settings
from django.utils import timezone, datetime_safe
from utils.models import Commit
from rest_framework.test import APIClient


class BaseTest(TestCase):

    def setUp(self):
        self.username = 'username'
        self.email = 'email@email.email'
        self.password = 'ER5dd[]433-444e'

        self.user = get_user_model().objects.create(
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=True
        )

        self.user_admin = get_user_model().objects.create(
            username=f"admin{self.username}",
            email=f"admin{self.email}",
            password=self.password,
            is_active=True,
            is_superuser=True,
            is_staff=True
        )

        self.request = RequestFactory
        self.request.user = self.user
        self.context = {'request': self.request}

        self.lang = settings.LANGUAGES_DEFAULT
        self.__available_langs = [lang[0] for lang in settings.LANGUAGES]
        self.lang2 = [lang for lang in self.__available_langs if lang is not self.lang][0]
        self.time = timezone.now()
        self.time2 = timezone.now() - timezone.timedelta(days=9)

        self.date = datetime_safe.new_date(self.time)
        self.date2 = datetime_safe.new_date(self.time2)

        self.factory = APIClient()
        self.factory.force_authenticate(user=self.user)
        self.factory_admin = APIClient()
        self.factory_admin.force_authenticate(user=self.user_admin)

    def get_user(self):
        return get_user_model().objects.get(
            username=self.username,
            email=self.email,
            password=self.password,
        )

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
