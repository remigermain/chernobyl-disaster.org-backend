from django.test import tag
from utils.serializers.contact import ContactSerializer
from lib.test import BaseTest


@tag('model', 'contact')
class ContactTest(BaseTest):

    def test_create_serializer(self):
        data = {
            'message': 'lalalalalal',
            'email': 'test@test.fr',
        }
        serializer = ContactSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.message, data['message'])
        self.check_creator(obj)

    def test_create_serializer_not_connected(self):
        data = {
            'message': 'lalalalalal',
            'email': 'test@test.fr'
        }
        serializer = ContactSerializer(data=data, context=self.get_anonymous_user())
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.message, data['message'])
        self.assertIsNone(obj.creator)
        self.assertEqual(obj.email, data['email'])

    def test_create_serializer_not_connected_empty_mail(self):
        data = {
            'message': 'lalalalalal',
        }
        serializer = ContactSerializer(data=data, context=self.get_anonymous_user())
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty(self):
        data = {}

        serializer = ContactSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
