from lib.viewset import ModelViewSetBase
from rest_framework.viewsets import ModelViewSet
from utils.models import Contact, Issue
from utils.serializers import contact, issue


class IssueViewSet(ModelViewSetBase):
    queryset = Issue.objects.none()
    serializer_class = issue.IssueSerializer


class ContactViewSet(ModelViewSet):
    # remove auth , all people can contact me :D
    permission_classes = []

    http_method_names = [r'post']
    queryset = Contact.objects.none()
    serializer_class = contact.ContactSerializer
