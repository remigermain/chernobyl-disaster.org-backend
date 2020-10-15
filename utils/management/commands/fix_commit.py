from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utils.models import Commit
from common.models import Tag, TagLang, Translate, TranslateLang
from timeline.models import Event, EventLang
from gallery.models import Character, CharacterLang, Picture, PictureLang, Video, VideoLang
from utils.function import contenttypes_uuid


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = get_user_model().objects.get(id=1)

        models = [
            Tag, TagLang, Translate, TranslateLang, Event, EventLang,
            Character, CharacterLang, Picture, PictureLang, Video, VideoLang
        ]

        total = {'delete': 0, 'create': {}}
        for commit in Commit.objects.all():
            if not commit.content_object:
                commit.delete()
                total['delete'] += 1

        bulk = []
        for model in models:
            for obj in model.objects.all():
                uuid = contenttypes_uuid(obj)
                if not Commit.objects.filter(uuid=uuid).exists():
                    bulk.append(Commit(
                        creator=user,
                        uuid=uuid,
                        content_object=obj
                    ))
                    key = model.__name__.lower()
                    if key not in total['create']:
                        total['create'][key] = 1
                    else:
                        total['create'][key] += 1
        Commit.objects.bulk_create(bulk)
        print(total)
