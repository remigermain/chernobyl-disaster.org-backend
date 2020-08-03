from lib.serializers  import ModelSerializerBase
from timeline.models import Document, DocumentLang


class DocumentLangSerializer(ModelSerializerBase):
    class Meta:
        model = DocumentLang
        fields = ['title', 'language']


class DocumentSerializer(ModelSerializerBase):
    langs = DocumentLangSerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = ['title', 'tags', 'event', 'doc', 'langs']


class DocumentSerializerPost(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        pass


class DocumentSerializerGet(DocumentSerializerPost):
    class Meta(DocumentSerializerPost.Meta):
        pass
