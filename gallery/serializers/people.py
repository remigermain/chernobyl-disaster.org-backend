from lib.serializers import ModelSerializerBase
from rest_framework.serializers import SerializerMethodField
from gallery.models import People, PeopleLang
from common.serializers.tag import TagSerializerMini


class PeopleLangSerializer(ModelSerializerBase):
    class Meta:
        model = PeopleLang
        fields = ['id', 'biography', 'language']


class PeopleSerializer(ModelSerializerBase):
    langs = PeopleLangSerializer(many=True, required=False)
    profil = SerializerMethodField()

    class Meta:
        model = People
        fields = ['id', 'name', 'born', 'death', 'profil', 'langs', 'tags']

    def get_profil(self, obj):
        if not obj.profil:
            return None
        return {
            'original_jpeg': obj.profil.url,
            'original_webp': obj.profil_webp.url,
            'thumbnail_webp': obj.profil_thumbnail_webp.url,
            'thumbnail_jpeg': obj.profil_thumbnail_jpeg.url,
        }


class PeopleSerializerPost(PeopleSerializer):
    tags = TagSerializerMini(many=True, required=False)
    profil = None

    class Meta(PeopleSerializer.Meta):
        pass


class PeopleSerializerMini(PeopleSerializer):
    class Meta(PeopleSerializer.Meta):
        fields = ['id', 'name']
