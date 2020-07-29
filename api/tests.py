from django.test import TestCase, tag
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.urls import reverse


@tag('login')
class Auth(TestCase):
    def test_register(self):
        data = {
            'username': 'username',
            'email': 'email@email.email',
            'password1': 'ApasswordAb123',
            'password2': 'ApasswordAb123',
        }
        # check response
        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)

        # check user will be create
        user = User.objects.filter(username=data['username'])
        self.assertEqual(user.count(), 1)
        user = user.first()
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])

        email = EmailAddress.objects.filter(email=user.email)
        self.assertEqual(email.count(), 1)

    def test_register_exsit(self):
        self.test_register()
        data = {
            'username': 'username',
            'email': 'email@email.email',
            'password1': 'ApasswordAb123',
            'password2': 'ApasswordAb123',
        }

        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 400)

    def test_register_wrong_password(self):
        data = {
            'username': 'username',
            'email': 'email@email.email',
            'password1': 'ApasswordAb123',
            'password2': 'ApasswogggggrdAb123',
        }

        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['non_field_errors'])

    def test_register_simply_password(self):
        data = {
            'username': 'username',
            'email': 'email@email.email',
            'password1': 'password',
            'password2': 'password',
        }

        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['password1'])

    def test_register_wrong_email(self):
        data = {
            'username': 'username',
            'email': 'email@email',
            'password1': 'ApasswordAb123',
            'password2': 'ApasswordAb123',
        }

        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['email'])

    def test_register_wrong_username(self):
        data = {
            'username': '',
            'email': 'email@email.email',
            'password1': 'ApasswordAb123',
            'password2': 'ApasswordAb123',
        }

        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['username'])

    def test_register_no_data(self):
        data = {}

        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['username'])
        self.assertIsNotNone(response.data['password1'])
        self.assertIsNotNone(response.data['password2'])

    def test_register_no_email(self):
        data = {
            'username': 'username',
            'password1': 'ApasswordAb123',
            'password2': 'ApasswordAb123',
        }

        response = self.client.post(reverse('rest_register'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.data)
        self.assertIsNotNone(response.data['email'])