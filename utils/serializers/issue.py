from lib.serializers import ModelSerializerBase
from utils.models import Issue
from django.core.exceptions import ValidationError


class IssueSerializer(ModelSerializerBase):
    class Meta:
        model = Issue
        fields = ['uuid', 'message', 'object_id']

    def get_contenttype(self, model, pk):
        return model.objects.get(pk=pk)

    def commit_create(self, *args):
        pass

    def commit_update(self, *args):
        pass

    def get_model(self, obj):
        return obj.contenttype.__class__ if obj.contenttype else None

    def validate_uuid(self, value):
        from django.contrib.contenttypes.models import ContentType

        try:
            return ContentType.objects.get(model=value).model_class()
        except ContentType.DoesNotExist as e:
            raise ValidationError(e)

    def validate(self, data):
        try:
            return {
                'content_object': self.get_contenttype(data['uuid'], data['object_id']),
                'message': data['message']
            }
        except data['uuid'].DoesNotExist as e:
            raise ValidationError(e)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return Issue.objects.create(**validated_data)
