from utils.function import contenttypes_uuid
from utils.models import Commit


def delete_commit(sender, **kwargs):
    uuid = contenttypes_uuid(kwargs['instance'])
    Commit.objects.filter(uuid=uuid).delete()


def create_tag(sender, **kwargs):
    from common.models import Tag, TagLang

    instance = kwargs['instance']
    field_name = instance.tag_fields

    def get_field_value(instance, field_name):
        return getattr(instance, field_name)[:Tag.name.field.max_length]

    value = get_field_value(instance, field_name[0])
    tag = Tag.objects.filter(name=value).first()

    if not tag:
        tag = Tag.objects.create(name=value)
        if len(field_name) == 2:
            bulk = []
            for obj in instance.langs.all():
                name = get_field_value(obj, field_name[1])
                bulk.append(TagLang(name=name, tag=tag))
            TagLang.objects.bulk_create(bulk)
    instance.tags.add(tag)
