from django.test import tag
from lib.test import BaseTest
from utils.serializers.issue import IssueSerializer
from django.urls import reverse
from django.utils import timezone
from timeline.models import Event
from utils.models import Issue
import json


@tag('issue')
class IssueTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(title="event_name", date=timezone.now())
        self.uuid = self.event.__class__.__name__.lower()

    @tag('auth')
    def test_auth(self):
        response = self.client.get(reverse('issue-list'))
        self.assertEqual(response.status_code, 403)
        response = self.factory.get(reverse('issue-list'))
        self.assertEqual(response.status_code, 405)

    def test_create_serializer(self):
        data = {
            'message': 'lalalalalal',
            'uuid': self.uuid,
            'object_id': self.event.id,
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_not_commit_created(instance)
        return instance

    def test_create_serializer_no_message(self):
        data = {
            'uuid': self.uuid,
            'object_id': self.event.id,
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_wrong_uuid(self):
        data = {
            'message': 'lalalalalal',
            'uuid': "uuid",
            'object_id': self.event.id,
        }
        serializer = IssueSerializer(data=data, context=self.get_anonymous_user())
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_no_uuid(self):
        data = {
            'message': 'lalalalalal',
            'object_id': self.event.id,
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_message(self):
        data = {
            'message': '',
            'uuid': self.uuid,
            'object_id': self.event.id,
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('client', 'create')
    def test_create_client(self):
        data = {
            'message': 'lalalalalal',
            'uuid': self.uuid,
            'object_id': self.event.id,
        }
        response = self.factory.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        obj = Issue.objects.get(id=content['id'])
        self.check_creator(obj)
        self.check_not_commit_created(obj)

    @tag('client', 'create')
    def test_create_client_no_message(self):
        data = {
            'uuid': self.uuid,
            'object_id': self.event.id,
        }
        response = self.factory.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_empty_message(self):
        data = {
            'message': '',
            'uuid': self.uuid,
            'object_id': self.event.id,
        }
        response = self.factory.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_no_uuid(self):
        data = {
            'message': 'lalalalalal',
            'object_id': self.event.id,
        }
        response = self.factory.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_wrong_uuid(self):
        data = {
            'message': 'lalalalalal',
            'uuid': "uuid",
            'object_id': self.event.id,
        }
        response = self.factory.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_wrong_object_id(self):
        data = {
            'message': 'lalalalalal',
            'uuid': self.uuid,
            'object_id': self.event.id + 1,
        }
        response = self.factory.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_wrong_emoty_object_id(self):
        data = {
            'message': 'lalalalalal',
            'uuid': self.uuid,
        }
        response = self.factory.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'get')
    def test_create_client_no_connect(self):
        data = {
            'message': 'lalalalalal',
            'uuid': self.uuid,
            'object_id': self.event.id,
        }
        response = self.client.post(reverse("issue-list"), data=data)
        self.assertEqual(response.status_code, 403)
