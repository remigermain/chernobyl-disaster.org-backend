from lib.serializers import ModelSerializerBase
from utils.models import Contact


class ContactSerializer(ModelSerializerBase):
    class Meta:
        model = Contact
        fields = ['message', 'email']

    def add_validated_data(self, validated_data):
        if self.context["request"].user.is_authenticated:
            validated_data['creator'] = self.context['request'].user
        return validated_data
