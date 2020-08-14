from rest_framework.parsers import MultiPartParser
from .mixins import ParserKeyDimensional
from .dict import QueryDimentionalNested
from django.http.multipartparser import MultiPartParserError
from rest_framework.exceptions import ParseError


class ParserMultiDimensional:

    def __init__(self, data):
        self.data = data
        self.valid = None

    def is_valid(self):
        self._post = QueryDimentionalNested()
        self.valid = False
        print(self.data)
        print("--------------------------------")
        for key, value in self.data.items():
            try:
                parser = ParserKeyDimensional(key)
                if not parser.is_valid():
                    return False
                parser.construct(self._post, self.data.getlist(key))
            except Exception as e:
                MultiPartParserError(e)
        print(self._post)
        print("--------------- END  -----------------")
        self.valid = True
        return self.valid

    @property
    def validate_data(self):
        if self.valid is None:
            raise ValueError("You need to be call is_valid() before access validate_data")
        return self._post


class NestedMultiPartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        parsed = super().parse(stream, media_type, parser_context)

        copy = parsed.data.copy()
        try:
            parser = ParserMultiDimensional(copy)
            if parser.is_valid():
                return parser.validate_data
        except MultiPartParserError as exc:
            raise ParseError('Multipart form parse error - %s' % str(exc))
        return parsed
