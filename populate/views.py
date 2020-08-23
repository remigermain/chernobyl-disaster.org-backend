from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from timeline.models import Event
from common.models import Tag, People, Commit
import random


def serialize(obj, display_name):
    return {'value': obj.id, 'display_name': getattr(obj, display_name)}


class PictureView(APIView):
    def get(self, request, format=None):
        return Response({
            'photographer': [serialize(obj, 'name') for obj in People.objects.all()]
        })

class PeopleView(APIView):
    def get(self, request, format=None):
        lst = [
            {'id': p.id, 'name': p.name, 'profil': p.to_url('profil')} for p in People.objects.all()
        ]
        random.shuffle(lst)
        return Response({'peoples': lst[:5]})

class PopulateView(APIView):

    def get(self, request, format=None):

        langs = [{'value': lang[0], 'display_name': lang[1]} for lang in settings.LANGUAGES]

        tags = [serialize(tag, 'name') for tag in Tag.objects.all()]
        events = [serialize(event, 'title') for event in Event.objects.all()]

        return Response({
            'langs': langs,
            'tags': tags,
            'events': events
        })


class ContributorView(APIView):
    def get(self, request, format=None):
        contributors = Commit.objects.values_list('creator__username', flat=True).distinct()
        return Response({'results': contributors})
