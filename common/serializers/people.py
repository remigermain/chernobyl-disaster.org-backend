from lib.serializers  import ModelSerializerBase
from common.models import People, PeopleLang


class PeopleLangSerializer(ModelSerializerBase):
    class Meta:
        model = PeopleLang
        fields = ['biography', 'people']


class PeopleSerializer(ModelSerializerBase):
    langs = PeopleLangSerializer(many=True, required=False)

    class Meta:
        model = People
        fields = ['name', 'born', 'death', 'profil', 'wikipedia', 'langs']


class PeopleSerializerPost(ModelSerializerBase):
    class Meta(PeopleSerializer.Meta):
        pass


class PeopleSerializerGet(PeopleSerializerPost):
    class Meta(PeopleSerializerPost.Meta):
        pass
