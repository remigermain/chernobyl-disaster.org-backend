from lib.viewset import ModelViewSetBase
from common.models import Tag, TagLang, Translate, TranslateLang
from lib.permission import UpdateOnly
from common.serializers import tag, translate


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer_class = tag.TagSerializer
    serializer_class_get = tag.TagSerializerGet
    serializer_class_post = tag.TagSerializerPost
    filterset_fields = ['name']
    search_fields = ['name']


class TagLangViewSet(ModelViewSetBase):
    queryset = TagLang.objects.all()
    serializer_class = tag.TagSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class TranslateViewSet(ModelViewSetBase):
    queryset = Translate.objects.all()
    serializer_class = translate.TranslateSerializer
    permission_class = (UpdateOnly,)


class TranslateLangViewSet(ModelViewSetBase):
    queryset = TranslateLang.objects.all()
    serializer_class = translate.TranslateLangSerializer
