from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from utils.models import Commit
from django.forms.models import model_to_dict


class ModelSerializerBaseNested(WritableNestedModelSerializer):
    def __init__(self, *args, **kwargs):
        if hasattr(self.Meta, 'fields'):
            if 'id' not in self.Meta.fields:
                self.Meta.fields.insert(0, 'id')  # allway add id

        super().__init__(*args, **kwargs)

    def validate_langs(self, data):
        """
            replace of unique together and constaits for language
        """
        objects = self.get_initial().get('langs', None)
        _raise = False

        def check_obj(obj):
            if isinstance(obj['id'], str) and not obj['id'].isdigit():
                return False
            return int(obj['id']) == lang['id']

        if self.instance:
            list_id = list(filter(lambda obj: 'id' in obj, objects))
            list_id_exist = []
            for lang in self.instance.langs.values('id', 'language'):
                current = list(filter(check_obj, list_id))
                if not current:
                    objects.append(lang)
                else:
                    list_id_exist.append(lang['id'])

            # if other id refered by not in this instance, raise error
            if len(list_id_exist) != len(list_id):
                _raise = True

        unique = list(set([obj.get('language', None) for obj in objects]))
        unique = list(filter(lambda x: x, unique))
        if _raise or len(unique) != len(objects):
            field = self.Meta.model.langs.field.model.language.field
            params = {
                'model_name': self.Meta.model.__name__,
                'field_label': capfirst(field.verbose_name)
            }
            raise ValidationError(
                message="101",
                code='unique',
                params=params,
            )
        return data

    def compare_field(self, instance, validated_data):
        """
            find where field are changed
        """
        diff = []
        for field, value in validated_data.items():
            relation = instance._meta.get_field(field)
            attr = getattr(instance, field)
            if relation.many_to_many:
                lst = list(attr.all())
                for element in lst:
                    el = list(filter(lambda x: x.id == element.id, value))
                    if not el:
                        diff.append(field)
                    else:
                        child = self.compare_field(element, model_to_dict(el[0]))
                        if child:
                            diff.extend(child)
                if len(lst) != len(value):
                    diff.append(field)
            elif relation.many_to_one and attr:
                if self.compare_field(attr, model_to_dict(value)):
                    diff.append(field)
            elif attr != value:
                diff.append(field)
        return diff

    def commit_create(self, request, obj):
        Commit.objects.create(creator=request.user, content_object=obj, created=True)

    def commit_update(self, request, obj, diff_fields):
        if diff_fields:
            updated_field = "|".join(diff_fields)
            Commit.objects.create(creator=request.user, content_object=obj, updated_field=updated_field)

    def create(self, validated_data):
        obj = super().create(validated_data)
        self.commit_create(self.context['request'], obj)
        return obj

    def update(self, instance, validated_data):
        diff_fields = self.compare_field(instance, validated_data)
        obj = super().update(instance, validated_data)

        # clean multi select tags
        if hasattr(self.Meta.model, 'tags') and 'tags' not in validated_data:
            obj.tags.clear()

        # we create a commit with contributor
        self.commit_update(self.context['request'], obj, diff_fields)
        return obj


class ModelSerializerBase(ModelSerializerBaseNested):
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', None)
        if context and \
           hasattr(context['request'], 'query_params') and \
           hasattr(context['request'].query_params, 'contribute') and \
           hasattr(self.Meta, 'fields') and \
           hasattr(self.Meta.model, "langs"):
            self.Meta.fields.extend([
                'available_languages',
                'not_available_languages'
                ])

        super().__init__(*args, **kwargs)

    commit_count = serializers.SerializerMethodField()
    available_languages = serializers.SerializerMethodField()
    not_available_languages = serializers.SerializerMethodField()

    def get_not_available_languages(self, obj):
        # get all langs available
        langs = [lang[0] for lang in obj.langs.model.lang_choices]
        # remove languages exsits
        langs_not_exist = list(set([o.language for o in obj.langs.all()]) ^ set(langs))
        langs_not_exist.sort()
        return langs_not_exist

    def get_available_languages(self, obj):
        # remove languages exsits
        langs_exist = [o.language for o in obj.langs.all()]
        langs_exist.sort()
        return langs_exist

    def get_commit_count(self, obj):
        # obj has annotate contributures count we return it or by queryset
        return obj.commit_count

    def updated(self, obj):
        # obj has annotate contributures count we return it or by queryset
        return obj.updated
