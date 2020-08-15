from lib.serializers  import ModelSerializerBase
from common.models import People, PeopleLang
from django.conf import settings
import os


class PeopleLangSerializer(ModelSerializerBase):
    class Meta:
        model = PeopleLang
        fields = ['biography', 'people']


class PeopleSerializer(ModelSerializerBase):
    langs = PeopleLangSerializer(many=True, required=False)

    class Meta:
        model = People
        fields = ['name', 'born', 'death', 'profil', 'wikipedia', 'langs']

    def get_profil(self, obj):
        if not obj.profil:
            return None
        return os.path.join(settings.SITE_URL, obj.profil.url)


class PeopleSerializerPost(ModelSerializerBase):
    class Meta(PeopleSerializer.Meta):
        pass


class PeopleSerializerGet(PeopleSerializerPost):
    class Meta(PeopleSerializerPost.Meta):
        pass
