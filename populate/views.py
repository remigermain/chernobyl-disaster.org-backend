from rest_framework.response import Response
from django.conf import settings
from timeline.models import Event
from gallery.models import Picture, Video, People
from common.models import Tag, Commit, Translate, TranslateLang
from django.db.models import Q, Count, F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from lib.permission import ReadOnlyLamda
from django.contrib.auth import get_user_model
from django.utils import timezone


def serialize(obj, display_name):
    return {'value': obj.id, 'display_name': getattr(obj, display_name)}


@api_view(['GET'])
def picture(request):
    return Response({
        'photographers': [serialize(obj, 'name') for obj in People.objects.all()]
    })


@api_view(['GET'])
def people(request):
    lst = [
        {
            'id': p.id,
            'name': p.name,
            'profil': p.to_url('profil'),
        }
        for p in People.objects.all().order_by('name')
    ]
    return Response({'peoples': lst})


@api_view(['GET'])
def populate(request):
    langs = [{'value': lang[0], 'display_name': lang[1]} for lang in settings.LANGUAGES]

    tags = [serialize(tag, 'name') for tag in Tag.objects.all()]
    events = [serialize(event, 'title') for event in Event.objects.all()]

    return Response({
        'langs': langs,
        'tags': tags,
        'events': events
    })

@api_view(['GET'])
def contributor(request):
    return Response({
        'results': Commit.objects.values_list('creator__username', flat=True).distinct()
    })


@api_view(['GET'])
def overview(request):
    week = timezone.now() - timezone.timedelta(days=7)

    query_week = [
        *get_user_model().objects.annotate(
            week=(
                Count("commit_creator", filter=Q(commit_creator__created__gte=week)) +
                Count("event_creator", filter=Q(event_creator__created__gte=week)) +
                Count("eventlang_creator", filter=Q(eventlang_creator__created__gte=week)) +
                Count("people_creator", filter=Q(people_creator__created__gte=week)) +
                Count("peoplelang_creator", filter=Q(peoplelang_creator__created__gte=week)) +
                Count("picture_creator", filter=Q(picture_creator__created__gte=week)) +
                Count("picturelang_creator", filter=Q(picturelang_creator__created__gte=week)) +
                Count("tag_creator", filter=Q(tag_creator__created__gte=week)) +
                Count("taglang_creator", filter=Q(taglang_creator__created__gte=week)) +
                Count("video_creator", filter=Q(video_creator__created__gte=week)) +
                Count("videolang_creator", filter=Q(videolang_creator__created__gte=week))
            ),
        ).values("username", "week"),
        *get_user_model().objects.annotate(
            week=Count("translatelang_creator", filter=Q(translatelang_creator__created__gte=week))
        ).values("username", "week"),
    ]

    query_total = [
        *get_user_model().objects.annotate(
            total=(
                Count("commit_creator") +
                Count("event_creator") +
                Count("eventlang_creator") +
                Count("people_creator") +
                Count("peoplelang_creator") +
                Count("picture_creator") +
                Count("picturelang_creator") +
                Count("taglang_creator") +
                Count("tag_creator") +
                Count("video_creator") +
                Count("videolang_creator")
            )
        ).values("username", "total"),
        *get_user_model().objects.annotate(total=Count("translatelang_creator")).values("username", "total"),
    ]

    def merge(query, annotate):
        dtc = {}
        for w in query:
            print(w)
            if w['username'] not in dtc:
                dtc[w['username']] = w[annotate]
            else:
                dtc[w['username']] += w[annotate]
        lst = [{'username': key, annotate: value} for key, value in dtc.items()]
        lst.sort(key=lambda x: x[annotate], reverse=True)
        lst = lst[:3]

        final = {}
        if len(lst) > 0:
            final['first'] = {'username': lst[0]['username'], 'count': lst[0][annotate]}
        if len(lst) > 1:
            final['second'] = {'username': lst[1]['username'], 'count': lst[1][annotate]}
        if len(lst) > 2:
            final['third'] = {'username': lst[2]['username'], 'count': lst[2][annotate]}
        return final

    lst_week = merge(query_week, "week")
    lst_total = merge(query_total, "total")

    default = ["creator__username", "created", "id", "display"]
    # add model field

    def generate(model, display):
        def update(obj, uuid):
            obj.update({"uuid": uuid})
            obj["creator"] = obj.pop("creator__username")
            obj["date"] = obj.pop("created")
            return obj
        uuid = model.__name__.lower()
        query = model.objects.all()\
                             .order_by("-created")\
                             .annotate(display=F(display))\
                             .select_related('creator').values(*default)
        return [update(obj, uuid) for obj in query[:50]]

    history = [
        *generate(Event, "title"),
        *generate(Picture, "title"),
        *generate(Video, "title"),
        *generate(Tag, "name"),
        *generate(People, "name"),
        *generate(Translate, "key"),
        *[
            {
                'id': obj.object_id,
                'creator': obj.username,
                'date': obj.created,
                'display': str(obj.content_object),
                'uuid': obj.content_object.__class__.__name__.lower(),
            }
            for obj in Commit.objects
                             .filter(~Q(uuid__contains="lang"))
                             .order_by("-created")
                             .annotate(username=F("creator__username"))
                             .select_related('creator')[:50]
        ]
    ]
    history.sort(key=lambda x: x['date'], reverse=True)

    query = {
        'week': lst_week,
        'total': lst_total,
        'results': history[:50]
    }
    return Response(query)


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

    deleted = 'on' in request.data['deleted'] if 'deleted' in request.data else False
    merged = 'on' in request.data['merge'] if 'merge' in request.data else False
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
        'removed': 0,
        'update': 0
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
        trans_exist = TranslateLang.objects.filter(language=language)\
                                           .prefetch_std()\
                                           .values_list('parent_key__key', flat=True)
        trans = list(Translate.objects.all())
        diff, exist = [], []
        for el in lst:
            if el['path'] in trans_exist:
                exist.append(el)
            else:
                diff.append(el)

        if merged:
            bulk_update = []
            for ex in TranslateLang.objects.filter(language=language).prefetch_std():
                el = list(filter(lambda o: ex.parent_key.key == o['path'], lst))
                if el:
                    ex.value = el[0]['value']
                    bulk_update.append(ex)
            data['update'] = len(bulk_update)
            TranslateLang.objects.bulk_update(bulk_update, ["value"])

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
