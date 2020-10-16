from django.apps import AppConfig
from django.db.models.signals import post_delete


class CommonConfig(AppConfig):
    name = 'common'

    def ready(self):
        from lib.signals import delete_commit
        from common.models import TranslateLang, Tag, TagLang
        post_delete.connect(delete_commit, sender=TranslateLang)
        post_delete.connect(delete_commit, sender=Tag)
        post_delete.connect(delete_commit, sender=TagLang)
