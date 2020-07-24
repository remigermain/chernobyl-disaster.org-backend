from core.drf import ModelViewSetBase
from .models import Event, EventLang, Picture, Document, Video, Article, \
    PictureLang, DocumentLang, VideoLang, ArticleLang
from .serializer import EventSerializer, EventLangSerializer, \
    PictureSerializer, DocumentSerializer, VideoSerializer, ArticleSerializer, \
    PictureLangSerializer, DocumentLangSerializer, VideoLangSerializer, ArticleLangSerializer
#  event


class EventViewSet(ModelViewSetBase):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventLangViewSet(ModelViewSetBase):
    queryset = EventLang.objects.all()
    serializer_class = EventLangSerializer


# extra in event


class PictureViewSet(ModelViewSetBase):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureLangViewSet(ModelViewSetBase):
    queryset = PictureLang.objects.all()
    serializer_class = PictureLangSerializer


class DocumentViewSet(ModelViewSetBase):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DocumentLangViewSet(ModelViewSetBase):
    queryset = DocumentLang.objects.all()
    serializer_class = DocumentLangSerializer


class VideoViewSet(ModelViewSetBase):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoLangViewSet(ModelViewSetBase):
    queryset = VideoLang.objects.all()
    serializer_class = VideoLangSerializer


class ArticleViewSet(ModelViewSetBase):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleLangViewSet(ModelViewSetBase):
    queryset = ArticleLang.objects.all()
    serializer_class = ArticleLangSerializer
