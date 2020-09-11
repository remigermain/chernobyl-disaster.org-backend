from django.test import tag
from common.serializers.issue import IssueSerializer
from common.models import Issue
from lib.utils import contenttypes_uuid
from lib.test import BaseTest


@tag('uuid', 'issue')
class IssueTest(BaseTest):

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'uuid': 'user',
            'object_id': self.user.pk,
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # check is create
        issue = Issue.objects.filter(uuid=contenttypes_uuid(Issue, self.user))
        self.assertEqual(issue.count(), 1)
        issue = issue.first()
        self.assertEqual(issue.content_object, self.user)
        self.assertEqual(issue.creator, self.user)

    @tag('serializer')
    def test_create_serializer_unk_model(self):
        data = {
            'uuid': 'usereee',
            'object_id': self.user.pk,
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_not_model(self):
        data = {
            'object_id': self.user.pk,
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_pk(self):
        data = {
            'uuid': 'user',
            'object_id': 'erfer',
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_pk2(self):
        data = {
            'uuid': 'user',
            'object_id': -5,
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_not_pk(self):
        data = {
            'uuid': 'user',
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_not_message(self):
        data = {
            'uuid': 'user',
            'object_id': self.user.pk
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())