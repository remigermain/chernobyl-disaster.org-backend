from rest_framework.viewsets import ModelViewSet
from lib.viewset import ModelViewSetBase
from common.models import Tag, TagLang, People, Issue, Contact, PeopleLang
from common.serializers import people, tag, issue, contact


class TagViewSet(ModelViewSetBase):
    queryset = Tag.objects.all()
    serializer_class = tag.TagSerializer
    serializer_class_get = tag.TagSerializerGet
    serializer_class_post = tag.TagSerializerPost
    filterset_fields = ['name']
    search_fields = ['name']


class TagLangViewSet(ModelViewSetBase):
    queryset = TagLang.objects.all()
    serializer_class = tag.TagSerializer
    filterset_fields = ['name']
    search_fields = ['name']


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


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.none()
    serializer_class = issue.IssueSerializer

    def get_queryset(self):
        # you can only delete/update/get yourqueryset
        return super().get_queryset().filter(creator=self.request.user)


class ContactViewSet(ModelViewSet):
    # remove auth , all people can contact me :D
    permission_classes = []

    http_method_names = [r'post']
    queryset = Contact.objects.none()
    serializer_class = contact.ContactSerializer
