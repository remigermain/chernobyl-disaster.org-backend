from lib.serializers  import ModelSerializerBase
from timeline.models import Document, DocumentLang
from django.conf import settings
import os


class DocumentLangSerializer(ModelSerializerBase):
    class Meta:
        model = DocumentLang
        fields = ['title', 'language']


class DocumentSerializer(ModelSerializerBase):
    langs = DocumentLangSerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = ['title', 'tags', 'event', 'doc', 'langs']

    def get_doc(self, obj):
        return os.path.join(settings.SITE_URL, obj.doc.url)


class DocumentSerializerPost(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        pass


class DocumentSerializerGet(DocumentSerializerPost):
    class Meta(DocumentSerializerPost.Meta):
        pass
