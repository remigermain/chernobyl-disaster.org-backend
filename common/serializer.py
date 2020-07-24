from core.drf import ModelSerializerBase
from .models import Tag, TagLang, People


class TagSerializer(ModelSerializerBase):
    class Meta:
        model = Tag
        fields = ['name']


class TagLangSerializer(ModelSerializerBase):
    class Meta:
        model = TagLang
        fields = ['name', 'tag']


class PeopleSerializer(ModelSerializerBase):
    class Meta:
        model = People
        fields = ['name']
