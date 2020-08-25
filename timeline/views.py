from lib.viewset import ModelViewSetBase
from timeline.models import Event, EventLang, Picture, Document, Video, Article, \
    PictureLang, DocumentLang, VideoLang, ArticleLang
from timeline.serializers import picture, article, document, event, video


class EventViewSet(ModelViewSetBase):
    queryset = Event.objects.all().order_by('date')
    serializer_class = event.EventSerializer
    serializer_class_get = event.EventSerializerGet
    serializer_class_post = event.EventSerializerPost
    filterset_fields = ['title', 'date']
    search_fields = ['title', 'date', 'langs__title', 'langs__description']
    ordering_fields = ['title', 'date']


class EventLangViewSet(ModelViewSetBase):
    queryset = EventLang.objects.all()
    serializer_class = event.EventLangSerializer
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'description']
    ordering_fields = ['title']


# extra in event

class PictureViewSet(ModelViewSetBase):
    queryset = Picture.objects.all()
    serializer_class = picture.PictureSerializer
    serializer_class_get = picture.PictureSerializerGet
    serializer_class_post = picture.PictureSerializerPost
    filterset_fields = ['title', 'event', 'photographer']
    search_fields = ['title', 'event__title', 'event__langs__title', 'event__langs__description', 'photographer__name', 'langs__title']
    ordering_fields = ['title', 'date', 'event__date', 'id']


class PictureLangViewSet(ModelViewSetBase):
    queryset = PictureLang.objects.all()
    serializer_class = picture.PictureLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title']
    ordering_fields = ['title']


class DocumentViewSet(ModelViewSetBase):
    queryset = Document.objects.all()
    serializer_class = document.DocumentSerializer
    serializer_class_get = document.DocumentSerializerGet
    serializer_class_post = document.DocumentSerializerPost
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event__title', 'event__langs__title', 'event__langs__description', 'langs__title']
    ordering_fields = ['title']


class DocumentLangViewSet(ModelViewSetBase):
    queryset = DocumentLang.objects.all()
    serializer_class = picture.PictureLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title']
    ordering_fields = ['title']


class VideoViewSet(ModelViewSetBase):
    queryset = Video.objects.all()
    serializer_class = video.VideoSerializer
    serializer_class_get = video.VideoSerializerGet
    serializer_class_post = video.VideoSerializerPost
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event__title', 'event__langs__title', 'event__langs__description', 'langs__title']
    ordering_fields = ['title']


class VideoLangViewSet(ModelViewSetBase):
    queryset = VideoLang.objects.all()
    serializer_class = video.VideoLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title']
    ordering_fields = ['title']


class ArticleViewSet(ModelViewSetBase):
    queryset = Article.objects.all()
    serializer_class = article.ArticleSerializer
    serializer_class_get = article.ArticleSerializerGet
    serializer_class_post = article.ArticleSerializerPost
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event__title', 'event__langs__title', 'event__langs__description', 'langs__title']
    ordering_fields = ['title']


class ArticleLangViewSet(ModelViewSetBase):
    queryset = ArticleLang.objects.all()
    serializer_class = article.ArticleLangSerializer
    filterset_fields = ['title', 'extra']
    search_fields = ['title']
    ordering_fields = ['title']
