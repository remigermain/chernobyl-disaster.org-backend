from lib.drf import ModelSerializerBase
from .models import Tag, TagLang, People, Issue, Contact
from django.core.exceptions import ValidationError
from rest_framework import serializers


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


class PeopleSerializer(ModelSerializerBase):
    class Meta:
        model = People
        fields = ['name']


class IssueSerializer(ModelSerializerBase):
    model = serializers.CharField()
    pk = serializers.IntegerField()

    class Meta:
        model = Issue
        fields = ['model', 'message', 'pk']

    def get_contenttype(self, model, pk):
        return model.objects.get(pk=pk)

    def validate_model(self, value):
        from django.contrib.contenttypes.models import ContentType

        try:
            return ContentType.objects.get(model=value).model_class()
        except ContentType.DoesNotExist as e:
            raise ValidationError(e)

    def validate(self, data):
        try:
            return {
                'content_object': self.get_contenttype(data['model'], data['pk']),
                'message': data['message']
            }
        except data['model'].DoesNotExist as e:
            raise ValidationError(e)


class ContactSerializer(ModelSerializerBase):
    class Meta:
        model = Contact
        fields = ['message']
