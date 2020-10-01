from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utils.models import Commit
from common.models import Tag, TagLang, Translate, TranslateLang
from timeline.models import Event, EventLang
from gallery.models import People, PeopleLang, Picture, PictureLang, Video, VideoLang


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = get_user_model().objects.get(id=1)

        models = [
            Tag, TagLang, Translate, TranslateLang, Event, EventLang,
            People, PeopleLang, Picture, PictureLang, Video, VideoLang
        ]

        dict_model = {}
        for m in models:
            dict_model[m.__name__.lower()] = m

        total = {'delete': {}, 'create': {}}

        bulk = []
        for commit in Commit.objects.all():
            if not commit.content_object:
                uuid = commit.uuid.split('|')
                obj = dict_model[uuid[1]].objects.filter(id=uuid[2])
                if not obj.exists():
                    commit.delete()
                    if not uuid[1] in total['delete']:
                        total['delete'][uuid[1]] = 1
                    else:
                        total['delete'][uuid[1]] += 1
                else:
                    obj = obj.get()
                    bulk.append(Commit(creator=user, content_object=obj, uuid=uuid, created=True))
                    if not uuid[1] in total['create']:
                        total['create'][uuid[1]] = 1
                    else:
                        total['create'][uuid[1]] += 1
        Commit.objects.bulk_create(bulk)
        print(total)
