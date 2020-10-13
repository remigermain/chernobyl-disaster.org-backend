from lib.serializers import ModelSerializerBase
from common.models import News
from rest_framework.serializers import SerializerMethodField


class NewsSerializer(ModelSerializerBase):
    author = SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'text', 'date', 'author']

    def get_author(self, obj):

        return str(obj.author)
