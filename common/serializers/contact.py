from lib.serializers import ModelSerializerBase
from common.models import Contact


class ContactSerializer(ModelSerializerBase):
    class Meta:
        model = Contact
        fields = ['message']

    def add_validated_data(self, validated_data):
        # add create if user is connected
        if self.context['request'].user.is_authenticated:
            validated_data['creator'] = self.context['request'].user
        return validated_data
