from lib.viewset import ModelViewSetBase
from common.models import Tag, Translate, TranslateLang
from lib.permission import ReadOnlyLamda, ChernobylPermission
from rest_framework.permissions import IsAuthenticated
from common.serializers import tag, translate


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer_class = tag.TagSerializer
    filterset_fields = ['name', 'langs__name']
    search_fields = ['name', 'langs__name']

    def get_queryset(self):
        return super().get_queryset().prefetch_related("langs")


class TranslateViewSet(ModelViewSetBase):
    queryset = Translate.objects.all()
    serializer_class = translate.TranslateSerializer
    permission_classes = (ReadOnlyLamda,)
    search_fields = ['langs__language']
    filterset_fields = ['langs__language']

    def get_queryset(self):
        return super().get_queryset().prefetch_related("langs")


class TranslateLangViewSet(ModelViewSetBase):
    queryset = TranslateLang.objects.all()
    serializer_class = translate.TranslateLangSerializer
    permission_classes = (ChernobylPermission, IsAuthenticated)
