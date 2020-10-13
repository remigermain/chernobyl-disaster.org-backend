from lib.viewset import ModelViewSetBase
from gallery.models import Picture, Video, People, PictureLang, VideoLang, PeopleLang
from gallery.serializers import picture, video, people
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import mixins, viewsets


class PictureLangViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PictureLang.objects.all()
    serializer_class = picture.PictureLangSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class PictureViewSet(ModelViewSetBase):
    queryset = Picture.objects.all()
    serializer_class = picture.PictureSerializer
    serializer_class_post = picture.PictureSerializerPost
    serializer_class_contribute = picture.PictureSerializerMini
    filterset_fields = ['id', 'title', 'event']
    search_fields = [
                    'title', 'event__title', 'event__langs__title', 'event__langs__description',
                    'langs__title', 'tags__name', 'tags__langs__name'
                ]
    ordering_fields = ['id', 'title', 'date', 'event__date']

    def get_queryset(self):
        return super().get_queryset()\
                      .prefetch_related("langs", "tags__langs")\
                      .select_related("event")


class VideoLangViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = VideoLang.objects.all()
    serializer_class = video.VideoLangSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class VideoViewSet(ModelViewSetBase):
    queryset = Video.objects.all()
    serializer_class = video.VideoSerializer
    serializer_class_post = video.VideoSerializerPost
    serializer_class_contribute = video.VideoSerializerMini
    filterset_fields = ['id', 'title', 'event']
    search_fields = [
                    'title', 'event__title', 'event__langs__title', 'event__langs__description',
                    'langs__title', 'tags__name', 'tags__langs__name'
                ]
    ordering_fields = ['id', 'title']

    def get_queryset(self):
        return super().get_queryset()\
                      .prefetch_related("langs", "tags__langs")\
                      .select_related("event")


class PeopleLangViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PeopleLang.objects.all()
    serializer_class = people.PeopleLangSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class PeopleViewSet(ModelViewSetBase):
    queryset = People.objects.all()
    serializer_class = people.PeopleSerializer
    serializer_class_post = people.PeopleSerializerPost
    serializer_class_contribute = people.PeopleSerializerMini
    filterset_fields = ['id', 'name', 'born', 'death']
    search_fields = ['name', 'born', 'death', 'langs__biography', 'tags__name', 'tags__langs__name']
    search_fields = ['name', 'born', 'death', 'langs__biography']

    def get_queryset(self):
        return super().get_queryset()\
                      .prefetch_related("langs", "tags__langs")
