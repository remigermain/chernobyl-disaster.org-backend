from lib.serializers  import ModelSerializerBase
from common.models import Contact


class ContactSerializer(ModelSerializerBase):
    class Meta:
        model = Contact
        fields = ['message']
