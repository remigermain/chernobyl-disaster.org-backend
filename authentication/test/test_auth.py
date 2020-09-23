from django.test import tag
from lib.test import BaseTest
from django.urls import reverse
import json


@tag('auth')
class AuthTest(BaseTest):

    def test_register_valid(self):
        data = {
            'username': 'username2',
            'email': 'email@email.fr',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 201)

    def test_register_empty(self):
        data = {}
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_register_witout_username(self):
        data = {
            'email': 'email@email.fr',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_register_witout_email(self):
        data = {
            'username': 'username2',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_register_witout_password(self):
        data = {
            'username': 'username2',
            'email': 'email@email.fr',
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_register_witout_password2(self):
        data = {
            'username': 'username2',
            'email': 'email@email.fr',
            'password1': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_register_no_same_password(self):
        data = {
            'username': 'username2',
            'email': 'email@email.fr',
            'password1': '5f5fwefFWFEd[[',
            'password2': '5f5fwefFWFE[[',
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        self.test_register_valid()
        data = {
            'username': 'username2',
            'password': self.password,
        }
        response = self.factory.post(reverse("rest_login"), data=data)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertIsNotNone(content['key'])

    def test_login_wrong(self):
        data = {
            'username': 'usernam',
            'password': self.password,
        }
        response = self.factory.post(reverse("rest_login"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_login_wrong2(self):
        data = {
            'username': 'username2',
            'password': self.password,
        }
        response = self.factory.post(reverse("rest_login"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_login_wrong3(self):
        data = {
            'username': 'username2',
        }
        response = self.factory.post(reverse("rest_login"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_login_wrong4(self):
        data = {
            'password': self.password,
        }
        response = self.factory.post(reverse("rest_login"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_login_delete(self):
        data = {
            'email': 'email@email.fr'
        }
        response = self.factory.post(reverse("rest_password_reset"), data=data)
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        data = {
            'email': 'email@email.fr'
        }
        response = self.factory.post(reverse("rest_password_reset"), data=data)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_wrong_email(self):
        data = {
            'email': 'email@emaifffffffffffffl.fr'
        }
        response = self.factory.post(reverse("rest_password_reset"), data=data)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_empty(self):
        data = {}
        response = self.factory.post(reverse("rest_password_change"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_reset_password_old_password(self):
        data = {
            "old_password": self.password,
            "new_password1": "5f5fwefFWFE[[",
            "new_password2": "5f5fwefFWFE[["
        }
        response = self.factory.post(reverse("rest_password_change"), data=data)
        self.assertEqual(response.status_code, 200)

    def test_auccount_delete(self):
        self.test_register_valid()
        response = self.factory.post(reverse("account_delete"))
        self.assertEqual(response.status_code, 200)
        user = self.get_user()
        self.assertFalse(user.is_active)

    def test_get_user(self):
        response = self.factory.get(reverse("rest_user_details"))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertDictEqual(
            content['scope'],
            {
                'staff': self.user.is_staff,
                'admin': self.user.is_superuser,
            }
        )
