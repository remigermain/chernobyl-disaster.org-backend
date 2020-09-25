from rest_framework import viewsets
from lib.parser.parser import NestedParser
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from distutils.util import strtobool
from lib.permission import ChernobylPermission
# from drf_nested_multipart_parser import NestedMultipartParser


class ModelViewSetBase(viewsets.ModelViewSet):
    parser_classes = (NestedParser, MultiPartParser, FormParser, JSONParser)
    permission_classes = (ChernobylPermission,)

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
        queryset = super().get_queryset()
        if completed is not None:
            if bool(strtobool(completed)):
                return queryset.completed()
            return queryset.uncompleted()
        return queryset

    def get_serializer_class(self, *args):
        """
            add new property in modelViewSet
            serializer_class_get and serializer_class_post
            change seriaizer by method name
        """
        actions = {
            'GET': 'serializer_class_get',
            'POST': 'serializer_class_post',
            'PATCH': 'serializer_class_post',
        }
        method = self.request.method.upper()
        if method in actions and hasattr(self, actions[method]):
            return getattr(self, actions[method])
        return super().get_serializer_class()
