from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from timeline.models import Event, Picture, Video
from common.models import Tag, People, Commit
from django.db.models import Q


def serialize(obj, display_name):
    return {'value': obj.id, 'display_name': getattr(obj, display_name)}


class PictureView(APIView):
    def get(self, request, format=None):
        return Response({
            'photographers': [serialize(obj, 'name') for obj in People.objects.all()]
        })


class PeopleView(APIView):
    def get(self, request, format=None):
        lst = [
            {
                'id': p.id,
                'name': p.name,
                'profil': p.to_url('profil'),
            }
            for p in People.objects.all().order_by('name')
        ]
        return Response({'peoples': lst})


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


class OverView(APIView):
    def get(self, request, format=None):
        UPDATE = "update"
        CREATE = "create"

        users = {}

        def gen_dtc(obj, type_obj, display=None, uuid=None):
            creator = str(obj.creator)
            if creator not in users:
                users[creator] = {UPDATE: 0, CREATE: 0}
            users[creator][type_obj] += 1
            return {
                'creator': str(obj.creator),
                'date': str(obj.created),
                'type': type_obj,
                'uuid': obj.__class__.__name__.lower() if not uuid else uuid.lower(),
                'object_id': obj.id if not display else display.id,
                'display': str(obj) if not display else str(display),
            }
        query = [
            gen_dtc(c, UPDATE, c.content_object, c.content_object.__class__.__name__)
            for c in Commit.objects.filter(~Q(uuid__contains="lang")).select_related('creator')
        ]

        query.extend([gen_dtc(c, CREATE) for c in Tag.objects.all().select_related('creator')])
        query.extend([gen_dtc(c, CREATE) for c in People.objects.all().select_related('creator')])
        query.extend([gen_dtc(c, CREATE) for c in Event.objects.all().select_related('creator')])
        query.extend([gen_dtc(c, CREATE) for c in Picture.objects.all().select_related('creator')])
        query.extend([gen_dtc(c, CREATE) for c in Video.objects.all().select_related('creator')])
        query.sort(key=lambda x: x['date'], reverse=True)
        data = {'results': query}

        contributor = [{'user': key, **value} for key, value in users.items()]

        contributor.sort(key=lambda x: x[CREATE], reverse=True)
        data[CREATE] = contributor[:3]

        contributor.sort(key=lambda x: x[UPDATE], reverse=True)
        data[UPDATE] = contributor[:3]
        return Response(data)
