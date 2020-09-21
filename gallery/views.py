from lib.viewset import ModelViewSetBase
from gallery.models import Picture, Video, PictureLang, VideoLang, People, PeopleLang
from gallery.serializers import picture, video, people


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


class PeopleViewSet(ModelViewSetBase):
    queryset = People.objects.all()
    serializer_class = people.PeopleSerializer
    serializer_class_get = people.PeopleSerializerGet
    serializer_class_post = people.PeopleSerializerPost
    filterset_fields = ['name', 'born', 'death']
    search_fields = ['name', 'born', 'death']


class PeopleLangViewSet(ModelViewSetBase):
    queryset = PeopleLang.objects.all()
    serializer_class = people.PeopleLangSerializer
    filterset_fields = ['biography']
    search_fields = ['biography']
