from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from utils.models import Commit
from rest_framework.fields import empty
from django.http import QueryDict


class ListSerializer(serializers.ListSerializer):
    def get_value(self, dictionary):
        if isinstance(dictionary, QueryDict):
            return dictionary.getlist(self.field_name, empty)
        return super().get_value(dictionary)


class ModelSerializerBaseNested(WritableNestedModelSerializer):

    def __init__(self, *args, **kwargs):
        setattr(self.Meta, 'list_serializer_class', ListSerializer)
        super().__init__(*args, **kwargs)
    
    def validate_langs(self, datas):
        """
            replace of unique together and constaits for language
        """
        def raise_error():
            field = self.Meta.model.langs.field.model.language.field
            raise ValidationError(
                message="101",
                code='unique',
                params={
                    'model_name': self.Meta.model.__name__,
                    'field_label': capfirst(field.verbose_name)
                },
            )

        # get actual language on models
        exist = []
        if self.instance:
            exist = list(self.instance.langs.all().values("id", "language"))

        news = []
        for item in self.get_initial().get('langs', []):
            pk = item.get('id', None)
            if pk:
                atc = list(filter(lambda o: o['id'] == int(pk), exist))[0]
                if not atc:
                    raise_error()
                # reasign language in current object
                atc['language'] = item.get('language')
            else:
                news.append(item.get('language'))

        # check if a same language
        for lang in news:
            atc = list(filter(lambda o: o['language'] == lang, exist))
            if atc:
                raise_error()

        if len(list(set(news))) != len(news):
            raise_error()
        
        return datas

    def __diff_field(self, old, new):
        """
            find field are changed before update
        """
        diff = []
        for field, value in old.items():
            if field not in new:
                diff.append(field)
            elif isinstance(field, list):
                for old_value, new_value in zip(value, new[field]):
                    if isinstance(old_value, dict):
                        diff.extend(self.__diff_field(old_value, new_value))
                    elif old_value != new_value:
                        diff.append(field)
            elif isinstance(field, dict):
                diff.extend(self.__diff_field(old[field], new[field]))
            elif value != new[field]:
                diff.append(field)
        return diff

    def commit_create(self, request, obj):
        Commit.objects.create(creator=request.user, content_object=obj, created=True)

    def commit_update(self, request, obj, diff):
        Commit.objects.create(creator=request.user, content_object=obj, updated_fields=diff)

    def create(self, validated_data):
        obj = super().create(validated_data)
        self.commit_create(self.context['request'], obj)
        return obj

    def update(self, instance, validated_data):
        # serialize old instance
        t1 = self.__class__(instance=instance).data

        obj = super().update(instance, validated_data)
        # clean multi select tags
        if hasattr(self.Meta.model, 'tags') and 'tags' not in validated_data:
            obj.tags.clear()

        # serialize new instance
        t2 = self.__class__(instance=obj).data

        # generate diff from old and new instance
        diff = self.__diff_field(t1, t2)
        # we create a commit with contributor
        if diff:
            self.commit_update(self.context['request'], obj, diff)
        return obj


class ModelSerializerBase(ModelSerializerBaseNested):
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', None)
        if context and hasattr(context['request'], 'query_params') and \
            'contribute' in context['request'].query_params and \
                hasattr(self.Meta.model, "langs"):
            self.Meta.fields.extend([
                'available_languages',
                'not_available_languages'
                ])

        super().__init__(*args, **kwargs)

    available_languages = serializers.SerializerMethodField()
    not_available_languages = serializers.SerializerMethodField()

    def get_not_available_languages(self, obj):
        exist = self.get_available_languages(obj)
        diff = list(set(exist) ^ set([lang[0] for lang in obj.langs.model.lang_choices]))
        diff.sort()
        return diff

    def get_available_languages(self, obj):
        langs_exist = [o.language for o in obj.langs.all()]
        langs_exist.sort()
        return langs_exist
