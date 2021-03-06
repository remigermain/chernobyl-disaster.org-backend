from lib.serializers import ModelSerializerBase
from common.models import Translate, TranslateLang


class TranslateLangSerializer(ModelSerializerBase):
    class Meta:
        model = TranslateLang
        fields = ['id', 'value', 'language', 'parent_key']


class TranslateSerializer(ModelSerializerBase):
    langs = TranslateLangSerializer(many=True, required=False)

    class Meta:
        model = Translate
        fields = ['id', 'key', 'langs']
