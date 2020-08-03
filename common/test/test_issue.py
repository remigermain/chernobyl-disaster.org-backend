from django.test import tag
from common.serializers.issue import IssueSerializer
from common.models import Issue
from lib.utils import contenttypes_uuid
from lib.test import BaseTest


@tag('model', 'issue')
class IssueTest(BaseTest):

    @tag('serializer')
    def test_create_serializer(self):
        data = {
            'model': 'user',
            'pk': self.user.pk,
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
            'model': 'usereee',
            'pk': self.user.pk,
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_not_model(self):
        data = {
            'pk': self.user.pk,
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_pk(self):
        data = {
            'model': 'user',
            'pk': 'erfer',
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_wrong_pk2(self):
        data = {
            'model': 'user',
            'pk': -5,
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_not_pk(self):
        data = {
            'model': 'user',
            'message': 'this is a repport!'
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('serializer')
    def test_create_serializer_not_message(self):
        data = {
            'model': 'user',
            'pk': self.user.pk
        }
        serializer = IssueSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())