from lib.serializers  import ModelSerializerBase
from common.models import People, PeopleLang
from django.conf import settings
import os


class PeopleLangSerializer(ModelSerializerBase):
    class Meta:
        model = PeopleLang
        fields = ['biography', 'language']


class PeopleSerializer(ModelSerializerBase):
    langs = PeopleLangSerializer(many=True, required=False)

    class Meta:
        model = People
        fields = ['name', 'born', 'death', 'profil', 'wikipedia', 'langs', 'tags']

    def get_profil(self, obj):
        if not obj.profil:
            return None
        return os.path.join(settings.SITE_URL, obj.profil.url)


class PeopleSerializerPost(PeopleSerializer):
    class Meta(PeopleSerializer.Meta):
        pass


class PeopleSerializerGet(PeopleSerializerPost):
    class Meta(PeopleSerializerPost.Meta):
        pass
