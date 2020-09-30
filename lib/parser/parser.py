from rest_framework.parsers import MultiPartParser
from django.http.multipartparser import MultiPartParserError
from django.http import QueryDict
import logging
import re

# create logger
logger = logging.getLogger("ParserMultiDimensional")


class ParserMultiDimensional:
    _reg_split = re.compile(r"(\[.*?\])")

    REG_NAME = r"\s*[a-zA-Z]\w*\s*"
    _reg_name = re.compile(r"^" + REG_NAME + r"$")

    REG_INDEX_LIST = r"\s*(\d+)?\s*"
    _reg_index_list = re.compile(r"^\[(" + REG_INDEX_LIST + r")\]$")  # can be number or nothing

    _reg_index_object = re.compile(r"^\[(" + REG_NAME + r")\]$")  # need to start with char + alpaha

    _reg_list = re.compile(r"^\[" + REG_INDEX_LIST + r"]$")
    _reg_object = re.compile(r"^\[" + REG_NAME + r"]$")

    def __init__(self, data):
        self.data = data
        self._valid = None

    def conv_list_index(self, key):
        ret = self._reg_index_list.search(key).groups()[0]
        if not ret:
            return -1
        return int(ret)

    def conv_object_index(self, key):
        return self._reg_index_object.search(key).groups()[0]

    def conv_index(self, index):
        if self.is_list(index):
            return self.conv_list_index(index)
        elif self.is_object(index):
            return self.conv_object_index(index)
        else:
            return index

    def is_list(self, key):
        if not key or self._reg_list.match(key):
            return True
        return False

    def is_object(self, key):
        if self._reg_object.match(key):
            return True
        return False

    def is_name(self, key):
        if self._reg_name.match(key):
            return True
        return False

    def split_key(self, key):
        # remove space
        key = key.replace(" ", "")
        results = self._reg_split.split(key)
        # remove empty string
        return list(filter(None, results))

    def valid_key(self, key):
        results = self.split_key(key)
        # not result or check first element
        if not results or not self.is_name(results[0]):
            return []
        for r in results[1:]:
            if not self.is_list(r) and not self.is_object(r):
                return []
        return results

    def set_type(self, dtc, key, value):
        index = self.conv_index(key)
        if self.is_list(key):
            if not len(dtc) or index == len(dtc):
                dtc.append(value)
                key = len(dtc) - 1
        elif index not in dtc:
            # TODO dict same as list
            dtc[index] = value
        return index

    def get_values(self, dtc, key):
        if isinstance(dtc, QueryDict):
            return dtc.getlist(key)
        return dtc.get(key)

    def construct(self, data):
        dictionary = {}

        for key, value in data.items():
            keys = self.valid_key(key)
            if not keys:
                logger.error(f"{self.__class__.__name__} error parsing {key} from {keys}")
                raise MultiPartParserError(f"invalid key {keys}")
            tmp = dictionary
            for curr, nxt in zip(keys, keys[1:]):
                set_type = [] if self.is_list(nxt) else {}
                tmp = tmp[self.set_type(tmp, curr, set_type)]
            self.set_type(tmp, keys[-1], self.get_values(data, key))
        self.__validate_data = dictionary
        return dictionary

    def is_valid(self):
        self._valid = False
        self.construct(self.data)
        self._valid = True
        return self._valid

    def _append_list(self, dtc, field, values):
        lst_mutable = []
        for ele in values:
            if isinstance(ele, dict):
                depth_dtc, lst_mutable = self._convert_to_querydict(ele)
                dtc.appendlist(field, depth_dtc)
            elif isinstance(ele, list):
                lst_mutable.extend(self._append_list(dtc, field, ele))
            else:
                dtc.appendlist(field, ele)
        return lst_mutable

    def _convert_to_querydict(self, data):
        dct = QueryDict(mutable=True)
        lst_mutable = [dct]
        for field, values in data.items():
            if isinstance(values, list):
                lst_mutable.extend(self._append_list(dct, field, values))
            else:
                dct.appendlist(field, values)
        return dct, lst_mutable

    def _set_mutable(self, query):
        """
            set mutable to false on all querydict
        """
        for dtc in query:
            dtc.mutable = False

    @property
    def validate_data(self):
        if self._valid is None:
            raise ValueError("You need to be call is_valid() before access validate_data")
        if self._valid is False:
            raise ValueError("You can't get validate data")
        dtc, mutable = self._convert_to_querydict(self.__validate_data)
        self._set_mutable(mutable)
        return dtc


class NestedParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        parsed = super().parse(stream, media_type, parser_context)

        copy = parsed.data.copy()
        if parsed.files:
            copy.update(parsed.files)
        parser = ParserMultiDimensional(copy)
        if parser.is_valid():
            return parser.validate_data
        return parsed
