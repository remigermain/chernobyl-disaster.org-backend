from django.apps import AppConfig


class TimelineConfig(AppConfig):
    name = 'timeline'

    def ready(self):
        from django.db.models.signals import post_delete
        from lib.signals import delete_commit
        from timeline.models import Event, EventLang
        post_delete.connect(delete_commit, sender=Event)
        post_delete.connect(delete_commit, sender=EventLang)
