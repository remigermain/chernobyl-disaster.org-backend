from django.test import tag
from lib.test import BaseTest
from utils.serializers.contact import ContactSerializer
from django.urls import reverse
from utils.models import Contact
import json


@tag('contact')
class ContactTest(BaseTest):

    @tag('auth')
    def test_auth(self):
        response = self.client.get(reverse('contact-list'))
        self.assertEqual(response.status_code, 405)

        response = self.factory.get(reverse('contact-list'))
        self.assertEqual(response.status_code, 405)

    def test_create_serializer(self):
        data = {
            'message': 'lalalalalal',
            'email': 'test@test.fr',
        }
        serializer = ContactSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_not_commit_created(instance)
        return instance

    def test_create_serializer_not_connected(self):
        data = {
            'message': 'lalalalalal',
            'email': 'test@test.fr'
        }
        serializer = ContactSerializer(data=data, context=self.get_anonymous_user())
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.check_not_commit_created(instance)

    def test_create_serializer_empty_mail(self):
        data = {
            'message': 'lalalalalal',
        }
        serializer = ContactSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_wrong_mail(self):
        data = {
            'message': 'lalalalalal',
            'email': 'test@test'
        }
        serializer = ContactSerializer(data=data, context=self.get_anonymous_user())
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_no_message(self):
        data = {
            'email': 'test@test.fr'
        }
        serializer = ContactSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    def test_create_serializer_empty_message(self):
        data = {
            'message': '',
            'email': 'test@test.fr'
        }
        serializer = ContactSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())

    @tag('client', 'create')
    def test_create_client(self):
        data = {
            'message': 'message',
            'email': 'test@test.fr'
        }
        response = self.factory.post(reverse("contact-list"), data=data)
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content)
        obj = Contact.objects.get(id=content['id'])
        self.check_creator(obj)
        self.check_not_commit_created(obj)

    @tag('client', 'create')
    def test_create_client_no_message(self):
        data = {
            'email': 'test@test.fr'
        }
        response = self.factory.post(reverse("contact-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_empty_message(self):
        data = {
            'message': '',
            'email': 'test@test.fr'
        }
        response = self.factory.post(reverse("contact-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_no_email(self):
        data = {
            'message': '',
        }
        response = self.factory.post(reverse("contact-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_wrong_email(self):
        data = {
            'message': '',
            'email': 'test@test'
        }
        response = self.factory.post(reverse("contact-list"), data=data)
        self.assertEqual(response.status_code, 400)

    @tag('client', 'create')
    def test_create_client_get(self):
        response = self.factory.get(reverse("contact-list"))
        self.assertEqual(response.status_code, 405)

    @tag('client', 'get')
    def test_create_client_no_connect(self):
        data = {
            'message': 'lalalalalal',
            'email': 'test@test.fr',
        }
        response = self.client.post(reverse("contact-list"), data=data)
        self.assertEqual(response.status_code, 201)
