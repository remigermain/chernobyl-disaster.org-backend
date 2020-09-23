from rest_framework import mixins, viewsets
from utils.models import Contact, Issue
from utils.serializers import contact, issue
from lib.permission import CreateOnly


class IssueViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Issue.objects.none()
    permission_classes = (CreateOnly,)
    serializer_class = issue.IssueSerializer


class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # remove auth , all people can contact me :D
    permission_classes = ()
    queryset = Contact.objects.none()
    serializer_class = contact.ContactSerializer
