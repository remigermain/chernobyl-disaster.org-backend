from lib.drf import ModelSerializerBase
from .models import Tag, TagLang, People


class TagLangSerializer(ModelSerializerBase):
    class Meta:
        model = TagLang
        fields = ['name', 'tag']


class TagSerializer(ModelSerializerBase):
    class Meta:
        model = Tag
        fields = ['name']


class TagSerializerSafe(ModelSerializerBase):
    langs = TagLangSerializer(many=True)

    class Meta(TagSerializer.Meta):
        fields = TagSerializer.Meta.fields + ['langs']

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class PeopleSerializer(ModelSerializerBase):
    class Meta:
        model = People
        fields = ['name']
