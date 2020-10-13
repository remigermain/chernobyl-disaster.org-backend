from lib.viewset import ModelViewSetBase
from common.models import Tag, Translate, TranslateLang, TagLang, News
from lib.permission import ReadOnlyLamda, ChernobylPermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from common.serializers import tag, translate, news
from rest_framework import mixins, viewsets


class TagLangViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TagLang.objects.all()
    serializer_class = tag.TagLangSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer_class = tag.TagSerializer
    serializer_class_contribute = tag.TagSerializerMini
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


class NewsViewSet(ModelViewSetBase):
    queryset = News.objects.filter(is_active=True).select_related('author')
    serializer_class = news.NewsSerializer
    permission_classes = (ReadOnlyLamda, IsAuthenticated)
