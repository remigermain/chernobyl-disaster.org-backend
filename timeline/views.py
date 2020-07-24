from core.drf import ModelViewSetBase
from .models import Event, EventLang, Picture, Document, Video, Article
from .serializer import EventSerializer, EventLangSerializer, \
    PictureSerializer, DocumentSerializer, VideoSerializer, ArticleSerializer

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


class DocumentViewSet(ModelViewSetBase):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class VideoViewSet(ModelViewSetBase):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ArticleViewSet(ModelViewSetBase):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
