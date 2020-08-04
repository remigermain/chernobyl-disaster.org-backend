from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db.models import UniqueConstraint
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.exceptions import ValidationError
from django.utils.text import capfirst


class ModelSerializerBase(WritableNestedModelSerializer):
    def __init__(self, *args, **kwargs):
        if hasattr(self.Meta, 'fields') and 'id' not in self.Meta.fields:
            self.Meta.fields.insert(0, 'id')  # allway add id
        super().__init__(*args, **kwargs)

    def validate_langs(self, data):
        """
            replace of unique together and constaits for language
        """
        objects = self.get_initial().get('langs', None)
        if self.instance:
            for lang in self.instance.langs.values('id', 'language'):
                ret = list(filter(lambda obj: 'id' in obj and lang['id'] == obj['id'], objects))
                if not ret:
                    objects.append(lang)
        unique = list(set([obj['language'] for obj in objects]))
        if len(unique) != len(objects):
            field = self.Meta.model.langs.field.model.language.field
            params = {
                'model_name': self.Meta.model.__name__,
                'field_label': capfirst(field.verbose_name)
            }
            raise ValidationError(
                message=field.error_messages['unique'],
                code='unique',
                params=params,
            )
        return data

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)

        from common.models import Commit
        # we create a commit with contributor
        Commit.objects.create(creator=self.context['request'].user, content_object=obj)
        return obj


class ModelSerializerBaseGet(ModelSerializerBase):
    """
        base class for serializer,
        is add the creator when models will created,
        and add the contributors when models will updated
    """

    def __init__(self, *args, **kwargs):

        if hasattr(self.Meta, 'fields'):
            self.Meta.fields.extend([
                'created',
                'updated',
                'commit_count',
                'available_languages',
                'not_available_languages'
                ])

        super().__init__(*args, **kwargs)

    commit_count = serializers.SerializerMethodField()
    available_languages = serializers.SerializerMethodField()
    not_available_languages = serializers.SerializerMethodField()

    def get_not_available_languages(self, obj):
        # return all language available
        if hasattr(obj, "langs"):
            if hasattr(obj, "ann_langs_not_availabe"):
                return obj.ann_langs_not_availabe
            # get all langs available
            langs = [lang[0] for lang in obj.langs.model.lang_choices]
            # remove languages exsits
            for lang in obj.langs.all().values("language"):
                langs.pop(lang, None)
            return "|".join(langs)
        return None

    def get_available_languages(self, obj):
        # return all language available
        if hasattr(obj, "langs"):
            if hasattr(obj, "ann_langs_availabe"):
                return obj.ann_langs_availabe
            return "|".join([lang.language for lang in obj.langs.all().values("language")])
        return None

    def get_commit_count(self, obj):
        # obj has annotate contributures count we return it or by queryset
        return getattr(obj, 'ann_commit_count', obj.commit_count)

    def updated(self, obj):
        # obj has annotate contributures count we return it or by queryset
        return getattr(obj, 'ann_updated', obj.updated)
