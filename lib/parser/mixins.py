from .exeptions import ParserError
import re


class ParserKeyDimensional(object):

    _reg_split = re.compile(r"(\[.*?\])")
    _reg_name = re.compile(r"^\s*[a-zA-Z]\w*\s*$")
    _reg_list = re.compile(r"^\[\s*(?:[a-zA-Z]\w*|\d+)?\s*\]$")
    _reg_object = re.compile(r"^[a-zA-Z]\w*$")
    _reg_list_index = re.compile(r"^\d+$")
    _reg_key = re.compile(r"^(?:\[\s*)(\w+|\d+)?(?:\s*\])$")

    def __init__(self, data):
        self.valid = None
        self._data = data
        self._split = None

    def split(self):
        self._split = list(filter(None, self._reg_split.split(self._data)))
        return self._split

    def is_valid(self):
        self.valid = False
        if not self._split:
            self.split()

        if not len(self._split) or not self._reg_name.match(self._split[0]):
            return False

        for key in self._split[1:]:
            if not self._reg_split.match(key):
                return False
        self.valid = True
        return True

    def is_list(self, val):
        return not val or self._reg_list_index.match(val)

    def is_object(self, val):
        return False if not val else self._reg_object.match(val)

    def construct(self, dictionary, values):
        if self.valid is None:
            raise ValueError("You need to be call is_valid() before access validate_data")

        def get_value(val):
            return val if len(val) > 1 else val[0]

        def get_index(val):
            try:
                return self._reg_key.search(val).groups()[0]
            except Exception:
                raise ParserError

        def conv_list(val):
            return val if isinstance(val, list) else list(val)

        def recursive(dic, key, keys):
            if not keys:
                if key not in dic:
                    dic[key] = get_value(values)
                else:
                    dic[key] = conv_list(dic[key]) + values
                return
            index = get_index(keys[0])
            if self.is_list(index):
                if key not in dic:
                    index = len(dic[key]) if not index else index
                    dic[key] = []
                index = int(index)
                _len = len(dic[key])
                if _len > index + 1:
                    raise ParserError("key upper")
                if index == _len:
                    dic[key].insert(index, None)
                recursive(dic[key], index, keys[1:])
            elif self.is_object(index):
                if not dic[key]:
                    dic[key] = {}
                recursive(dic[key], index, keys[1:])
            else:
                raise ParserError("unknow type")
        recursive(dictionary, self._split[0], self._split[1:])
        return dictionary
