from rest_framework.viewsets import ModelViewSet
from lib.viewset import ModelViewSetBase
from common.models import Tag, TagLang, Translate, TranslateLang, Contact, Issue
from lib.permission import UpdateOnly
from common.serializers import tag, contact, issue, translate


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


class IssueViewSet(ModelViewSetBase):
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


class TranslateViewSet(ModelViewSetBase):
    queryset = Translate.objects.all()
    serializer_class = translate.TranslateSerializer
    permission_class = (UpdateOnly,)


class TranslateLangViewSet(ModelViewSetBase):
    queryset = TranslateLang.objects.all()
    serializer_class = translate.TranslateLangSerializer
