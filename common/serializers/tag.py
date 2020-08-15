from lib.serializers  import ModelSerializerBase
from common.models import Tag, TagLang


class TagLangSerializer(ModelSerializerBase):
    class Meta:
        model = TagLang
        fields = ['name', 'language']


class TagSerializer(ModelSerializerBase):
    langs = TagLangSerializer(many=True, required=False)

    class Meta:
        model = Tag
        fields = ['name', 'langs']


class TagSerializerPost(TagSerializer):
    class Meta(TagSerializer.Meta):
        pass


class TagSerializerGet(TagSerializerPost):
    class Meta(TagSerializerPost.Meta):
        pass
