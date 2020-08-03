from lib.serializers  import ModelSerializerBase
from common.models import Issue
from django.core.exceptions import ValidationError
from rest_framework import serializers


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
