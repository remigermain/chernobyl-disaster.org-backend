from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.sites.models import Site
from django.conf import settings
from .add_superuser import EMAIL, USERNAME


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # remove/add site name
        Site.objects.all().delete()
        Site.objects.create(
            domain=settings.DOMAIN_NAME,
            name=settings.SITE_NAME
        )

        # remove dev staff usser
        get_user_model().objects.filter(
            Q(username=USERNAME) | Q(email=EMAIL),
            is_staff=True
        )
