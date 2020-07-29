from django.test import tag
from common.serializer import ContactSerializer
from lib.test import BaseTest


@tag('model', 'contact')
class IssueTest(BaseTest):

    def test_create_serializer(self):
        data = {
            'message': 'lalalalalal'
        }
        serializer = ContactSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.message, data['message'])
        self.check_creator(obj)

    def test_create_serializer_empty(self):
        data = {}

        serializer = ContactSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())