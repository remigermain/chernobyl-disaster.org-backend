from lib.serializers import ModelSerializerBase
from rest_framework.serializers import SerializerMethodField
from gallery.models import Character, CharacterLang
from common.serializers.tag import TagSerializerMini


class CharacterLangSerializer(ModelSerializerBase):
    class Meta:
        model = CharacterLang
        fields = ['id', 'biography', 'language']


class CharacterSerializer(ModelSerializerBase):
    langs = CharacterLangSerializer(many=True, required=False)
    profil = SerializerMethodField()

    class Meta:
        model = Character
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


class CharacterSerializerPost(CharacterSerializer):
    tags = TagSerializerMini(many=True, required=False)
    profil = None

    class Meta(CharacterSerializer.Meta):
        pass


class CharacterSerializerMini(CharacterSerializer):
    class Meta(CharacterSerializer.Meta):
        fields = ['id', 'name']
