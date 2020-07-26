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


class EventLangViewSet(ModelViewSetBase):
    queryset = EventLang.objects.all()
    serializer_class = EventLangSerializer


# extra in event


class PictureViewSet(ModelViewSetBase):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    serializer_class_safe = PictureSerializerSafe


class PictureLangViewSet(ModelViewSetBase):
    queryset = PictureLang.objects.all()
    serializer_class = PictureLangSerializer


class DocumentViewSet(ModelViewSetBase):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    serializer_class_safe = DocumentSerializerSafe


class DocumentLangViewSet(ModelViewSetBase):
    queryset = DocumentLang.objects.all()
    serializer_class = DocumentLangSerializer


class VideoViewSet(ModelViewSetBase):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    serializer_class_safe = VideoSerializerSafe


class VideoLangViewSet(ModelViewSetBase):
    queryset = VideoLang.objects.all()
    serializer_class = VideoLangSerializer


class ArticleViewSet(ModelViewSetBase):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    serializer_class_safe = ArticleSerializerSafe


class ArticleLangViewSet(ModelViewSetBase):
    queryset = ArticleLang.objects.all()
    serializer_class = ArticleLangSerializer
