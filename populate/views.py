from rest_framework.response import Response
from django.conf import settings
from timeline.models import Event
from gallery.models import Character
from common.models import Tag, Translate, TranslateLang
from utils.models import Commit
from django.db.models import Q, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.utils import timezone
from utils.function import contenttypes_uuid
from django.contrib.auth import get_user_model
from lib.utils import to_bool


def serialize(obj, display_name):
    return {'value': obj.id, 'display_name': getattr(obj, display_name)}


@api_view(['GET'])
def characters(request):
    lst = [
        {
            'id': obj.id,
            'name': obj.name,
            'profil': {
                'thumbnail_webp': obj.profil_thumbnail_webp.url,
                'thumbnail_jpeg': obj.profil_thumbnail_jpeg.url,
            }
        }
        for obj in Character.objects.all().order_by('name')
    ]
    return Response({'characters': lst})


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
        'contributors': get_user_model().objects.annotate(count=Count('commit_creator'))
                                                .filter(
                                                    ~Q(username=settings.ADMIN_USERNAME),
                                                    count__gte=1
                                                 )
                                                .distinct()
                                                .order_by('username')
                                                .prefetch_related('commit_creator')
                                                .values_list('username', flat=True),
        'donors': get_user_model().objects.filter(amount__gte=1)
                                          .order_by('-amount')
                                          .values_list('username', flat=True)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overview(request):
    week = timezone.now() - timezone.timedelta(days=7)

    lst_week = get_user_model().objects\
                               .annotate(count=Count('commit_creator', filter=Q(commit_creator__date__gte=week)))\
                               .filter(~Q(username=settings.ADMIN_USERNAME), count__gte=1)\
                               .order_by('-count')\
                               .prefetch_related('commit_creator')\
                               .values('count', 'username')[:3]
    lst_total = get_user_model().objects\
                                .annotate(count=Count('commit_creator'))\
                                .filter(~Q(username=settings.ADMIN_USERNAME), count__gte=1)\
                                .order_by('-count')\
                                .prefetch_related('commit_creator')\
                                .values('count', 'username')[:3]

    def conv_uuid(obj):
        return obj.__class__.__name__.lower().replace("lang", "")

    def conv_id(obj):
        if isinstance(obj.content_object, TranslateLang):
            return obj.content_object.language
        return obj.content_object.get_commit_id

    def conv_query(obj):
        if isinstance(obj.content_object, TranslateLang):
            return {
                'params': {
                    'id': obj.content_object.language,
                },
                'query': {
                    'key': obj.content_object.parent_key.key.split('.')[0],
                    'id': obj.content_object.parent_key.id
                },
                'detail': False,
            }
        return {}

    history = [
        {
            'id': conv_id(commit),
            'creator': commit.creator.username,
            'date': commit.date,
            'display': str(commit.content_object),
            'uuid': conv_uuid(commit.content_object),
            'created': commit.created,
            'detail': True,
            **conv_query(commit)
        }
        for commit in Commit.objects.filter(creator__isnull=False)
                                    .prefetch_related("content_object")
                                    .order_by('-date')[:50]
    ]

    query = {   
        'week': lst_week,
        'total': lst_total,
        'results': history
    }
    return Response(query)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

    # generate uuids
    uuids = [contenttypes_uuid(t) for t in TranslateLang.objects.filter(language=lang)]
    deleted = TranslateLang.objects.filter(language=lang).delete()

    # delete commit
    Commit.objects.filter(uuid__in=uuids).delete()

    data = {"detail": deleted}
    return Response(data, status=HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def translate_json(request):
    import json

    language = None
    if 'language' in request.data:
        if request.data['language'] not in [code[0] for code in TranslateLang.lang_choices]:
            return Response(status=HTTP_400_BAD_REQUEST, data={'detail': "language not found"})
        language = request.data['language']

    try:
        content = json.loads(request.data['file'].read())
    except KeyError:
        return Response(status=HTTP_400_BAD_REQUEST, data={'detail': "file not found"})
    except Exception as error:
        return Response(status=HTTP_400_BAD_REQUEST, data={'detail': str(error)})

    deleted = to_bool(request.data['delete']) if 'delete' in request.data else False
    merged = to_bool(request.data['merge']) if 'merge' in request.data else False
    parent = to_bool(request.data['parent']) if 'parent' in request.data else False

    if 'percentage' in content:
        del content['percentage']

    def gen_path(path, key):
        return f"{path}.{key}" if path else key

    def depth_dict(path, element):
        if isinstance(element, dict):
            for key, value in element.items():
                depth_dict(gen_path(path, key), value)
        elif type(element) in [str, int]:
            lst.append({'path': path, 'value': element})
        else:
            raise TypeError(f"file type error {type(element)}")

    lst = []
    try:
        depth_dict("", content)
    except TypeError as e:
        return Response(status=HTTP_400_BAD_REQUEST, data={'detail': str(e)})

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
        bulk = [Translate(key=key) for key in diff]
        Translate.objects.bulk_create(bulk)
        data['created'] = len(diff)

    if language:
        trans_exist = TranslateLang.objects.filter(language=language)\
                                           .select_related('parent_key')\
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
            for ex in TranslateLang.objects.filter(language=language).select_related('parent_key'):
                el = list(filter(lambda o: ex.parent_key.key == o['path'], lst))
                # check if value is not a empty string
                if el:
                    ex.value = el[0]['value']
                    bulk_update.append(ex)
            data['update'] = len(bulk_update)
            TranslateLang.objects.bulk_update(bulk_update, ["value"])

        def find_parent(key):
            return list(filter(lambda o: o.key == key, trans))[0]

        bulk = [
            TranslateLang(
                value=obj['value'],
                language=language,
                parent_key=find_parent(obj['path'])
            )
            for obj in diff if obj['value']
        ]
        TranslateLang.objects.bulk_create(bulk)
        data['createdLang'] = len(bulk)

    # create first parent key
    if parent:
        def to_parent_key(key):
            key = key.split('.')[0]
            return f"menu-name.{key}"
        keys = [to_parent_key(key) for key in list_path]
        key_exists = Translate.objects.filter(key__in=keys).values_list('key', flat=True)
        diff = list(set(key_exists) ^ set(keys))
        bulk = [Translate(key=key) for key in diff]
        Translate.objects.bulk_create(bulk)
        data['createParentKeys'] = len(bulk)

    return Response(status=HTTP_200_OK, data=data)
