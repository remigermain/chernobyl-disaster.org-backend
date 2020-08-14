import re
from .exeptions import ParserError, OutOfRange, UnknowKey, UnknowType

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
        if not self._split:
            self.split()
        self.valid = False
        # check empty list
        if not len(self._split):
            return False
        # check first name
        if not self._reg_name.match(self._split[0]):
            return False
        for key in self._split[1:]:
            if not self._reg_split.match(key):
                return False
        self.valid = True
        return True

    def get_key(self, val):
        ret = self._reg_key.search(val)
        if not ret:
            raise ParserError("get_key return nothing")
        return ret.groups()[0]

    def is_list(self, val):
        return not val or self._reg_list_index.match(val)

    def is_object(self, val):
        return False if not val else self._reg_object.match(val)

    def construct(self, data, assign):
        if self.valid is None:
            raise ValueError("You need to be call is_valid() before access validate_data")

        def recursive(dtc, key, value):
            if not value:
                # print(f"-- asssing  {dtc} {key} ----\n")
                try:
                    dtc[key] = assign
                except IndexError:
                    raise OutOfRange("index out of range")
                return None
            _key = self.get_key(value[0])

            if self.is_list(_key):
                if key not in dtc:
                    dtc[key] = []
                if not _key:
                    _key = len(dtc[key])  # if _key is not set "[]", take the lenght value of list

                elif _key.isdigit():
                    _key = int(_key)
                    _len = len(dtc[key])

                    if _len > _key + 1:
                        # if key is upper than length of list like  list[5] but list as only 3 item
                        # raise a parse Error
                        raise UnknowKey("unknow list key")

                    if _key == _len:
                        # if not element in list , create one
                        dtc[key].insert(_key, None)
                    recursive(dtc[key], _key, value[1:])
                else:
                    raise UnknowKey("unknow list key")

            elif self.is_object(_key):
                if not dtc[key]:
                    dtc[key] = {}
                if _key not in dtc[key]:
                    dtc[key][_key] = None
                recursive(dtc[key], _key, value[1:])

            else:
                raise UnknowType(f"unknow Type of {_key}")

        recursive(data, self._split[0], self._split[1:])
        return data
