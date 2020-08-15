from rest_framework.parsers import MultiPartParser
from .mixins import ParserKeyDimensional
from django.http.multipartparser import MultiPartParserError
from rest_framework.exceptions import ParseError


class ParserMultiDimensional:

    def __init__(self, data):
        self.data = data
        self._valid = None

    def is_valid(self):
        self._post = dict()
        self._valid = False
        for key, value in self.data.items():
            try:
                parser = ParserKeyDimensional(key)
                if not parser.is_valid():
                    return False
                parser.construct(self._post, self.data.getlist(key))
            except Exception as e:
                MultiPartParserError(e)
        self._valid = True
        return self._valid

    @property
    def validate_data(self):
        if self._valid is None:
            raise ValueError("You need to be call is_valid() before access validate_data")
        if self._valid is False:
            raise ValueError("You can't get validate data")
        return self._post


class NestedMultiPartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        parsed = super().parse(stream, media_type, parser_context)

        copy = parsed.data.copy()
        if parsed.files:
            copy.update(parsed.files)
        try:
            parser = ParserMultiDimensional(copy)
            if parser.is_valid():
                data = parser.validate_data
                if 'tags' in data and not isinstance(data['tags'], list):
                    data['tags'] = [data['tags']]
                return data
        except MultiPartParserError as exc:
            raise ParseError('Multipart form parse error - %s' % str(exc))
        return parsed
