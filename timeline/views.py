from lib.viewset import ModelViewSetBase
from timeline.models import Event, EventLang
from timeline.serializers import event


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
