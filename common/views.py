from rest_framework.viewsets import ModelViewSet
from lib.drf import ModelViewSetBase
from .models import Tag, TagLang, People, Issue, Contact
from .serializer import TagLangSerializer, TagSerializer, PeopleSerializer, \
    TagSerializerSafe, IssueSerializer, ContactSerializer


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    serializer_class_safe = TagSerializerSafe
    filterset_fields = ['name']
    search_fields = ['name']


class TagLangViewSet(ModelViewSetBase):
    queryset = TagLang.objects.all()
    serializer_class = TagLangSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class PeopleViewSet(ModelViewSetBase):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    filterset_fields = ['name']
    search_fields = ['name']


class IssueViewSet(ModelViewSet):
    http_method_names = [r'post']
    queryset = Issue.objects.none()
    serializer_class = IssueSerializer


class ContactViewSet(ModelViewSet):
    http_method_names = [r'post']
    queryset = Contact.objects.none()
    serializer_class = ContactSerializer
