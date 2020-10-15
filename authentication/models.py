from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    amount = models.IntegerField(default=0)
    show_helpers = models.BooleanField(default=True)
    show_admin = models.BooleanField(default=False)

    lang_choices = settings.LANGUAGES
    lang_default = settings.LANGUAGES_DEFAULT
    default_language = models.CharField(choices=lang_choices, max_length=4, default=lang_default)
