from rest_framework.viewsets import ModelViewSet
from lib.drf import ModelViewSetBase
from .models import Tag, TagLang, People, Issue, Contact, PeopleLang
from .serializer import TagLangSerializer, TagSerializer, PeopleSerializer, \
    TagSerializerSafe, IssueSerializer, ContactSerializer, PeopleLangSerializer, \
    PeopleSerializerSafe


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
    serializer_class_safe = PeopleSerializerSafe
    filterset_fields = ['name', 'born', 'death']
    search_fields = ['name', 'born', 'death']


class PeopleLangViewSet(ModelViewSetBase):
    queryset = PeopleLang.objects.all()
    serializer_class = PeopleLangSerializer
    filterset_fields = ['biography']
    search_fields = ['biography']


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.none()
    serializer_class = IssueSerializer

    def get_queryset(self):
        # you can only delete/update/get yourqueryset
        return super().get_queryset().filter(creator=self.request.user)


class ContactViewSet(ModelViewSet):
    http_method_names = [r'post']
    queryset = Contact.objects.none()
    serializer_class = ContactSerializer
