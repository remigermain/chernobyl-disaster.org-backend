from rest_framework import viewsets
from lib.metadata import MetadataBase


class ModelViewSetBase(viewsets.ModelViewSet):
    # remove delete method
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace']
    metadata_class = MetadataBase

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
        """
            no paginate if no_page in query params
        """
        if 'no_page' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def get_serializer_class(self, *args):
        """
            add new property in modelViewSet
            serializer_class_get and serializer_class_post
            change seriaizer by method name
        """
        actions = [
            {'method': 'GET', 'serializer': 'serializer_class_get'},
            {'method': 'POST', 'serializer': 'serializer_class_post'},
            {'method': 'PUT', 'serializer': 'serializer_class_post'},
            {'method': 'PATCH', 'serializer': 'serializer_class_post'},
        ]
        print(self.request.data)
        print("\n")
        #if 'langs' in self.request.data:
            # import json
            # print(json.loads(self.request.data['langs'])['title'])
            # print(type(self.request.data['langs']))
        method = self.request.method.upper()
        for action in actions:
            if method == action['method'] and hasattr(self, action['serializer']):
                return getattr(self, action['serializer'])
        return super().get_serializer_class()
