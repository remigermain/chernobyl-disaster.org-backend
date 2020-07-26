from lib.drf import ModelViewSetBase
from .models import Tag, TagLang, People
from .serializer import TagLangSerializer, TagSerializer, PeopleSerializer, \
    TagSerializerSafe


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    serializer_class_safe = TagSerializerSafe
    filterset_fields = ['name']
    search_fields = ['name']


class TagLangViewSet(ModelViewSetBase):
    queryset = TagLang.objects.all()
    serializer_class = TagLangSerializer


class PeopleViewSet(ModelViewSetBase):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
