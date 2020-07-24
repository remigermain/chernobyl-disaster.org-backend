from core.drf import ModelViewSetBase
from .models import Tag, TagLang, People
from .serializer import TagLangSerializer, TagSerializer, PeopleSerializer


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer = TagSerializer


class TagLangViewSet(ModelViewSetBase):
    queryset = TagLang.objects.all()
    serializer = TagLangSerializer


class PeopleViewSet(ModelViewSetBase):
    queryset = People.objects.all()
    serializer = PeopleSerializer
