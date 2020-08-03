from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class ModelSerializerBase(ModelSerializer):
    def __init__(self, *args, **kwargs):
        if hasattr(self.Meta, 'fields'):
            # automatic add 'id' in fields and created, updated, contributors count methods
            self.Meta.fields.insert(0, 'id')
        super().__init__(*args, **kwargs)

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
