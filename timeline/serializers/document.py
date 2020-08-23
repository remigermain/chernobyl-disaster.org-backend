from lib.serializers import ModelSerializerBase
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

    def get_picture(self, obj):
        return {
            'full': obj.to_url('doc'),
            'thumbnail': obj.to_url('doc_thumbnail'),
        }


class DocumentSerializerPost(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        pass


class DocumentSerializerGet(DocumentSerializerPost):
    class Meta(DocumentSerializerPost.Meta):
        pass
