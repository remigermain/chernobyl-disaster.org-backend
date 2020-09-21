from lib.viewset import ModelViewSetBase
from gallery.models import Picture, Video, People
from gallery.serializers import picture, video, people


class PictureViewSet(ModelViewSetBase):
    queryset = Picture.objects.all()
    serializer_class = picture.PictureSerializer
    serializer_class_get = picture.PictureSerializerGet
    serializer_class_post = picture.PictureSerializerPost
    filterset_fields = ['title', 'event', 'photographer']
    search_fields = ['title', 'event__title', 'event__langs__title', 'event__langs__description', 'photographer__name', 'langs__title']
    ordering_fields = ['title', 'date', 'event__date', 'id']

    def get_queryset(self):
        return super().get_queryset()\
                      .prefetch_related(
                          "langs",
                          "tags__langs",
                      )\
                      .select_related(
                          "photographer",
                          "event",
                      )


class VideoViewSet(ModelViewSetBase):
    queryset = Video.objects.all()
    serializer_class = video.VideoSerializer
    serializer_class_get = video.VideoSerializerGet
    serializer_class_post = video.VideoSerializerPost
    filterset_fields = ['title', 'event']
    search_fields = ['title', 'event__title', 'event__langs__title', 'event__langs__description', 'langs__title']
    ordering_fields = ['title']

    def get_queryset(self):
        return super().get_queryset()\
                      .prefetch_related(
                          "langs",
                          "tags__langs"
                      )\
                      .select_related(
                          "event",
                      )


class PeopleViewSet(ModelViewSetBase):
    queryset = People.objects.all()
    serializer_class = people.PeopleSerializer
    serializer_class_get = people.PeopleSerializerGet
    serializer_class_post = people.PeopleSerializerPost
    filterset_fields = ['name', 'born', 'death']
    search_fields = ['name', 'born', 'death']

    def get_queryset(self):
        return super().get_queryset()\
                      .prefetch_related(
                          "langs",
                          "tags__langs"
                      )