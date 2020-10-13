from lib.viewset import ModelViewSetBase
from timeline.models import Event, EventLang
from timeline.serializers import event
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import mixins, viewsets


class EventLangViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = EventLang.objects.all()
    serializer_class = event.EventLangSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class EventViewSet(ModelViewSetBase):
    queryset = Event.objects.all().order_by('date')
    serializer_class = event.EventSerializer
    serializer_class_get = event.EventSerializerTimeline
    serializer_class_contribute = event.EventSerializerMini
    serializer_class_post = event.EventSerializerPost
    filterset_fields = ['title', 'date']
    search_fields = ['title', 'date', 'langs__title', 'langs__description', 'tags__name', 'tags__langs__name']
    ordering_fields = ['id', 'title', 'date']

    def get_queryset(self):
        fields = ["langs", "pictures__langs", "videos__langs", "tags__langs"]
        return super().get_queryset().prefetch_related(*fields)
