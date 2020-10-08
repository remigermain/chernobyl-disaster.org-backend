from lib.serializers import ModelSerializerBase
from common.models import Tag, TagLang


class TagLangSerializer(ModelSerializerBase):
    class Meta:
        model = TagLang
        fields = ['id', 'name', 'language']


class TagSerializer(ModelSerializerBase):
    langs = TagLangSerializer(many=True, required=False)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'langs']
        extra_kwargs = {
            'name': {'validators': []},
        }


class TagSerializerMini(TagSerializer):
    class Meta(TagSerializer.Meta):
        fields = ['id', 'name']
