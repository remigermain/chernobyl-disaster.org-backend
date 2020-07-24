from rest_framework import serializers, viewsets


class ModelSerializerBase(serializers.ModelSerializer):
    """
        base class for serializer,
        is add the creator when models will created,
        and add the contributors when models will updated
    """
    def __init__(self, *args, **kwargs):

        # we allway add the validatos for languages
        if hasattr(self.Meta.model, 'language'):
            if not hasattr(self.Meta, 'validators'):
                self.Meta.validators = []
            self.Meta.validators.append(
                serializers.UniqueTogetherValidator(
                    queryset=self.Meta.model.objects.all(),
                    fields=('language', self.Meta.model.get_parent_lang),
                )
            )

        super().__init__(*args, **kwargs)

    def save(self):
        contributor = False
        if not self.instance:
            # we add the creator
            self.validated_data['creator'] = self.context['request'].user
        elif self.instance.id:
            contributor = True
        obj = super().save()
        if contributor:
            # we add the contributor
            obj.contributors.add(self.context['request'].user)
        return obj


class ModelViewSetBase(viewsets.ModelViewSet):
    # remove delete method
    http_method_names = [u'get', u'post', u'put', u'patch', u'head', u'options', u'trace']
