from lib.drf import ModelViewSetBase
from .models import Event, EventLang, Picture, Document, Video, Article, \
    PictureLang, DocumentLang, VideoLang, ArticleLang
from .serializer import EventSerializer, EventLangSerializer, \
    PictureSerializer, DocumentSerializer, VideoSerializer, ArticleSerializer, \
    PictureLangSerializer, DocumentLangSerializer, VideoLangSerializer, ArticleLangSerializer, \
    EventSerializerSafe, PictureSerializerSafe, DocumentSerializerSafe, \
    ArticleSerializerSafe, VideoSerializerSafe


class EventViewSet(ModelViewSetBase):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    serializer_class_safe = EventSerializerSafe
    filterset_fields = ['title', 'date']
    search_fields = ['title', 'date']
    ordering_fields = ['title', 'date']


class EventLangViewSet(ModelViewSetBase):
    queryset = EventLang.objects.all()
    serializer_class = EventLangSerializer
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event']
    ordering_fields = ['title']


# extra in event


class PictureViewSet(ModelViewSetBase):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    serializer_class_safe = PictureSerializerSafe
    filterset_fields = ['title', 'event', 'photographer']
    search_fields = ['title', 'event', 'photographer']
    ordering_fields = ['title']


class PictureLangViewSet(ModelViewSetBase):
    queryset = PictureLang.objects.all()
    serializer_class = PictureLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title', 'extra']
    ordering_fields = ['title']


class DocumentViewSet(ModelViewSetBase):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    serializer_class_safe = DocumentSerializerSafe
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event']
    ordering_fields = ['title']


class DocumentLangViewSet(ModelViewSetBase):
    queryset = DocumentLang.objects.all()
    serializer_class = DocumentLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title', 'extra']
    ordering_fields = ['title']


class VideoViewSet(ModelViewSetBase):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    serializer_class_safe = VideoSerializerSafe
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event']
    ordering_fields = ['title']


class VideoLangViewSet(ModelViewSetBase):
    queryset = VideoLang.objects.all()
    serializer_class = VideoLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title', 'extra']
    ordering_fields = ['title']


class ArticleViewSet(ModelViewSetBase):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    serializer_class_safe = ArticleSerializerSafe
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event']
    ordering_fields = ['title']


class ArticleLangViewSet(ModelViewSetBase):
    queryset = ArticleLang.objects.all()
    serializer_class = ArticleLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title', 'extra']
    ordering_fields = ['title']
