from lib.serializers import ModelSerializerBase
from common.models import Contact
from django.db import models


class ContactSerializer(ModelSerializerBase):
    class Meta:
        model = Contact
        fields = ['message', 'email']

    def validate(self, validated_data):
        if not self.context['request'].user.is_authenticated:
            val = None if 'email' not in validated_data else validated_data['email']
            # run validator
            email = models.EmailField(null=False, blank=False)
            email.validate(val, None)
        return super().validate(validated_data)

    def add_validated_data(self, validated_data):
        # add create if user is connected
        if self.context['request'].user.is_authenticated:
            validated_data['creator'] = self.context['request'].user
        return validated_data
