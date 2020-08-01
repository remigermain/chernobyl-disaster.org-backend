from rest_framework import serializers, viewsets

NAME_REVERSE_LANG = 'langs'
NAME_LANG = 'language'


class ModelSerializerBase(serializers.ModelSerializer):
    """
        base class for serializer,
        is add the creator when models will created,
        and add the contributors when models will updated
    """

    def __init__(self, *args, **kwargs):

        if hasattr(self.Meta.model, NAME_LANG):

            self.Meta.fields.append(NAME_LANG)
        #     # we allway add the validatos for languages
        #     if not hasattr(self.Meta, 'validators'):
        #         self.Meta.validators = []
        #     self.Meta.validators.append(
        #         serializers.UniqueTogetherValidator(
        #             queryset=self.Meta.model.objects.all(),
        #             fields=(NAME_LANG, self.Meta.model.get_parent_lang),
        #         )
        #     )

        if hasattr(self.Meta, 'fields'):
            # automatic add 'id' in fields and created, updated, contributors count methods
            self.Meta.fields.insert(0, 'id')
            self.Meta.fields.extend([
                'created',
                'updated',
                'commit_count',
                'available_languages'
                ])

        super().__init__(*args, **kwargs)

    commit_count = serializers.SerializerMethodField()
    available_languages = serializers.SerializerMethodField()

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

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)

        from common.models import Commit
        # we create a commit with contributor
        Commit.objects.create(creator=self.context['request'].user, content_object=obj)
        return obj


class ModelViewSetBase(viewsets.ModelViewSet):
    # remove delete method
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace']
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'filterset_fields'):
            self.filterset_fields = []
        if not hasattr(self, 'search_fields'):
            self.search_fields = []
        if not hasattr(self, 'ordering_fields'):
            self.ordering_fields = []
        # we allway ad tags if models is not tags
        fields = ['id', 'created']

        from common.models import Tag, TagLang
        if self.get_model not in [Tag, TagLang] and hasattr(self.get_model, 'tags'):
            fields.extend(['tags__name'])
        if hasattr(self.get_model, 'language'):
            fields.append('language')
        if hasattr(self.get_model, 'langs'):
            fields.extend(['langs__language'])

        self.ordering_fields.extend(fields)
        self.search_fields.extend(fields)
        self.filterset_fields.extend(fields)

        super().__init__(*args, **kwargs)

    @property
    def get_model(self):
        # return model of class
        return self.serializer_class.Meta.model

    def paginate_queryset(self, queryset):
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def get_serializer_class(self, *args):
        """
            add new property in modelViewSet
            serializer_class_safe is the serializer for safe methods
            we change the serializer for SAFE methods
        """
        if self.request.method in self.SAFE_METHODS and hasattr(self, 'serializer_class_safe'):
            return self.serializer_class_safe
        return super().get_serializer_class()
