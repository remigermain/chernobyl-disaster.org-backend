from django.apps import AppConfig


class TimelineConfig(AppConfig):
    name = 'timeline'

    def ready(self):
        from django.db.models.signals import post_delete, post_save
        from lib.signals import delete_commit, create_tag
        from timeline.models import Event, EventLang
        post_delete.connect(delete_commit, sender=Event)
        post_delete.connect(delete_commit, sender=EventLang)

        post_save.connect(create_tag, sender=Event)
