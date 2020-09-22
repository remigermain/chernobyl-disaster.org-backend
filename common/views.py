from lib.viewset import ModelViewSetBase
from common.models import Tag, Translate, TranslateLang
from lib.permission import ReadOnlyLamda
from common.serializers import tag, translate


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer_class = tag.TagSerializer
    serializer_class_get = tag.TagSerializerGet
    serializer_class_post = tag.TagSerializerPost
    filterset_fields = ['name']
    search_fields = ['name']

    def get_queryset(self):
        return super().get_queryset().prefetch_related("langs")


class TranslateViewSet(ModelViewSetBase):
    queryset = Translate.objects.all()
    serializer_class = translate.TranslateSerializer
    permission_class = (ReadOnlyLamda,)

    def get_queryset(self):
        return super().get_queryset().prefetch_related("langs")


class TranslateLangViewSet(ModelViewSetBase):
    queryset = TranslateLang.objects.all()
    serializer_class = translate.TranslateLangSerializer
