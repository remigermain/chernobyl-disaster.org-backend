from django.test import tag
from lib.test import BaseTest
from django.urls import reverse
from django.core import mail
from django.conf import settings
from django.contrib.auth import get_user_model
import json


@tag('auth', 'authentication')
class AuthTest(BaseTest):

    def setUp(self):
        super().setUp()
        self.set_email_none()
        self.username = 'username'
        self.email = 'email@email.email'
        self.password = 'ER5dd[]433-444e'

    def set_email_mandatory(self):
        settings.ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

    def set_email_none(self):
        settings.ACCOUNT_EMAIL_VERIFICATION = 'none'

    def test_register_valid(self):
        data = {
            'username': 'username2',
            'email': 'email@email.fr',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 201)
        return data

    @tag('email', 'register')
    def test_register_valid_with_email(self):
        self.set_email_mandatory()
        data = {
            'username': 'username2',
            'email': 'email@email.fr',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)

    def test_register_same_username(self):
        self.test_register_valid()
        data = {
            'username': 'username2',
            'email': 'email@email.frf',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_register_same_email(self):
        self.test_register_valid()
        data = {
            'username': 'username25',
            'email': 'email@email.fr',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 400)

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

    def test_login_with_email_verification(self):
        self.test_register_valid_with_email()
        self.set_email_mandatory()
        data = {
            'username': 'username2',
            'password': self.password,
        }
        response = self.factory.post(reverse("rest_login"), data=data)
        self.assertEqual(response.status_code, 400)

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

    def test_reset_password(self):
        data = {
            'email': 'email@email.fr'
        }
        response = self.factory.post(reverse("rest_password_reset"), data=data)
        self.assertEqual(response.status_code, 200)

    def test_reset_password_with_email_dont_exits(self):
        self.set_email_mandatory()
        data = {
            'email': 'email@email.fr'
        }
        response = self.factory.post(reverse("rest_password_reset"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    @tag('email', 'password')
    def test_reset_password_with_email_exits(self):
        dict_instance = self.test_register_valid()
        self.set_email_mandatory()
        data = {
            'email': dict_instance['email']
        }
        response = self.factory.post(reverse("rest_password_reset"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

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

    def test_reset_password_wrong_old_password(self):
        data = {
            "old_password": self.password + "dd",
            "new_password1": "5f5fwefFWFE[[",
            "new_password2": "5f5fwefFWFE[["
        }
        response = self.factory.post(reverse("rest_password_change"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_reset_password_wrong_no_old_password(self):
        data = {
            "new_password1": "5f5fwefFWFE[[",
            "new_password2": "5f5fwefFWFE[["
        }
        response = self.factory.post(reverse("rest_password_change"), data=data)
        self.assertEqual(response.status_code, 400)

    def test_reset_password_wrong_no_same_password(self):
        data = {
            "old_password": self.password,
            "new_password1": "5f5fwefFWFE[dd[",
            "new_password2": "5f5fwefFWFE[["
        }
        response = self.factory.post(reverse("rest_password_change"), data=data)
        self.assertEqual(response.status_code, 400)

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

    def test_settings_change(self):
        data = {
            'show_helpers': True,
            'show_admin': False
        }
        response = self.factory.patch(reverse("rest_user_details"), data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.show_helpers)
        self.assertFalse(self.user.show_admin)

    def test_settings_change2(self):
        data = {
            'show_helpers': False,
            'show_admin': True
        }
        response = self.factory.patch(reverse("rest_user_details"), data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.show_helpers)
        self.assertTrue(self.user.show_admin)


@tag('auth', 'authentication')
class AuthTestDelete(BaseTest):

    def test_register_valid(self):
        data = {
            'username': 'username2',
            'email': 'email@email.fr',
            'password1': self.password,
            'password2': self.password,
        }
        response = self.factory.post(reverse("rest_register"), data=data)
        self.assertEqual(response.status_code, 201)
        return data

    def test_account_delete(self):
        self.test_register_valid()
        user = self.user
        response = self.factory.post(reverse("account_delete"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(id=user.id).exists())
