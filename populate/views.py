from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from timeline.models import Event, Picture, Video
from common.models import Tag, People, Commit, Translate, TranslateLang
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from lib.permission import ReadOnlyLamda


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


@api_view(['GET'])
@permission_classes([ReadOnlyLamda])
def translate_overview(request):
    data = {}
    for t in TranslateLang.lang_choices:
        data[t[0]] = 0
    count = 0
    for t in Translate.objects.all().prefetch_related('langs'):
        for lang in t.langs.all():
            data[lang.language] += 1
        count += 1
    submit = []
    for language in data:
        submit.append({
            'language': language,
            'object_id': language,
            'ratio': round(data[language] * 100 / count, 1) if count > 0 else 0
        })
    return Response(submit)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def translate_delete(request, lang):
    if lang not in [code[0] for code in TranslateLang.lang_choices]:
        return Response(status=HTTP_400_BAD_REQUEST, data={'detail': "language not found"})
    data = {
        "detail": TranslateLang.objects.filter(language=lang).delete()
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def translate_json(request):
    import json

    if 'file' not in request.data:
        return Response(status=HTTP_400_BAD_REQUEST, data={'detail': "file not found"})

    language = None
    if 'language' in request.data:
        if request.data['language'] not in [code[0] for code in TranslateLang.lang_choices]:
            return Response(status=HTTP_400_BAD_REQUEST, data={'detail': "language not found"})
        language = request.data['language']

    deleted = request.data['deleted'] == 'on' if 'deleted' in request.data else False
    content = json.loads(request.data['file'].read())

    def gen_path(path, key):
        return f"{path}.{key}" if path else key

    def depth_dict(path, element):
        if isinstance(element, dict):
            for key, value in element.items():
                depth_dict(gen_path(path, key), value)
        elif isinstance(element, str):
            lst.append({'path': path, 'value': element})
        else:
            raise TypeError(f"file type error {type(element)}")

    lst = []
    try:
        depth_dict("", content)
    except TypeError as e:
        return Response(status=HTTP_400_BAD_REQUEST, data={'detail': e})

    data = {
        'created': 0,
        'createdLang': 0,
        'removed': 0
    }

    list_path = [el['path'] for el in lst]
    if deleted:
        data['removed'] = Translate.objects.filter(~Q(key__in=list_path)).delete()[0]

    exist = Translate.objects.filter(key__in=list_path).values_list('key', flat=True)
    diff = list(set(exist) ^ set(list_path))

    if len(diff) > 0:
        bulk = [Translate(creator=request.user, key=key) for key in list_path]
        Translate.objects.bulk_create(bulk)
        data['created'] = len(diff)

    if language:
        trans_exist = TranslateLang.objects.filter(language=language).prefetch_std().values_list('parent_key__key', flat=True)
        trans = list(Translate.objects.all())
        diff = [el for el in lst if el['path'] not in trans_exist]

        def find_parent(key):
            return list(filter(lambda o: o.key == key, trans))[0]

        bulk = [
            TranslateLang(
                creator=request.user,
                value=obj['value'],
                language=language,
                parent_key=find_parent(obj['path'])
            )
            for obj in diff
        ]
        TranslateLang.objects.bulk_create(bulk)
        data['createdLang'] = len(bulk)

    return Response(status=HTTP_200_OK, data=data)
