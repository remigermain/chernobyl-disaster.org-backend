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
            # we allway add the validatos for languages
            if not hasattr(self.Meta, 'validators'):
                self.Meta.validators = []
            self.Meta.validators.append(
                serializers.UniqueTogetherValidator(
                    queryset=self.Meta.model.objects.all(),
                    fields=(NAME_LANG, self.Meta.model.get_parent_lang),
                )
            )

        if hasattr(self.Meta, 'fields'):
            # automatic add 'id' in fields and created, updated, contributors count methods
            self.Meta.fields.insert(0, 'id')
            self.Meta.fields.extend([
                NAME_LANG,
                'created',
                'updated',
                'contributors_count'
                ])

        super().__init__(*args, **kwargs)

    contributors_count = serializers.SerializerMethodField()

    def get_contributors_count(self, obj):
        # if obj has annotate contributures count we return it or by queryset
        if hasattr(obj, 'ann_contributors_count'):
            return obj.ann_contributors_count
        return obj.contributors.count()

    def save(self):
        contributor = False
        if not self.instance:
            # we add the creator
            self.validated_data['creator'] = self.context['request'].user
        elif self.instance.id:
            contributor = True
        # TODO
        obj = super().save()
        if contributor:
            # we add the contributor
            obj.contributors.add(self.context['request'].user)
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
        from common.models import Tag, TagLang
        if self.get_model not in [Tag, TagLang]:
            self.search_fields.append('tags__name')
            self.search_fields.append('tags')

        self.ordering_fields.extend(['created', 'updated'])

        super().__init__(*args, **kwargs)

    @property
    def get_model(self):
        # return model of class
        return self.serializer_class.Meta.model

    def get_serializer_class(self, *args):
        """
            add new property in modelViewSet
            serializer_class_safe is the serializer for safe methods
            we change the serializer for SAFE methods
        """
        if self.request.method in self.SAFE_METHODS and hasattr(self, 'serializer_class_safe'):
            return self.serializer_class_safe
        return super().get_serializer_class()
