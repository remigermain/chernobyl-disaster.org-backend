from rest_framework import viewsets
from drf_nested_forms.parsers import NestedMultiPartParser
from lib.parser.parser import NestedMultiPartParser as n
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from distutils.util import strtobool
from lib.permission import ChernobylPermission


class ModelViewSetBase(viewsets.ModelViewSet):
    parser_classes = (n, NestedMultiPartParser, MultiPartParser, FormParser, JSONParser)
    permission_classes = (ChernobylPermission,)

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
            fields.extend(['tags__name', 'tags__langs__name'])

        if hasattr(self.get_model, "langs"):
            self.search_fields.append('langs__language')

        self.ordering_fields.extend(fields)
        self.search_fields.extend(fields)
        self.filterset_fields.extend(fields)

        self.ordering_fields = list(set(self.ordering_fields))
        self.search_fields = list(set(self.search_fields))
        self.filterset_fields = list(set(self.filterset_fields))

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

    def get_queryset(self):
        """
            get queryset and filter on models if models has all languages availables
            with query params "completed"
            if true , you get all models has all languages,
            if false, you get all models need translate,
            if None , you get all
        """
        completed = self.request.query_params.get('completed', None)
        queryset = super().get_queryset().prefetch_std()
        if completed is not None:
            completed = bool(strtobool(completed))
            if completed:
                queryset = queryset.completed()
            else:
                queryset = queryset.uncompleted()
        return queryset

    def get_serializer_class(self, *args):
        """
            add new property in modelViewSet
            serializer_class_get and serializer_class_post
            change seriaizer by method name
        """
        actions = [
            {'method': 'GET', 'serializer': 'serializer_class_get'},
            {'method': 'POST', 'serializer': 'serializer_class_post'},
            {'method': 'PATCH', 'serializer': 'serializer_class_post'},
        ]
        method = self.request.method.upper()
        for action in actions:
            if method == action['method'] and hasattr(self, action['serializer']):
                return getattr(self, action['serializer'])
        return super().get_serializer_class()
