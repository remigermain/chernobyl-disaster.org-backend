from .exeptions import ParserError, OutOfRange, UnknowKey, UnknowType
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

    def get_key(self, val):
        ret = self._reg_key.search(val)
        if not ret:
            raise ParserError("get_key return nothing")
        return ret.groups()[0]

    def is_list(self, val):
        return not val or self._reg_list_index.match(val)

    def is_object(self, val):
        return False if not val else self._reg_object.match(val)

    def construct(self, dictionary, values):
        if self.valid is None:
            raise ValueError("You need to be call is_valid() before access validate_data")

        def get_value(val):
            return val if len(val) > 1 else val[0]

        def conv_list(val):
            return val if isinstance(val, list) else list(val)

        def recursive(dic, key, keys):
            if not keys:
                try:
                    if key not in dic:
                        dic[key] = get_value(values)
                    else:
                        dic[key] = conv_list(dic[key]) + values
                except IndexError:
                    raise OutOfRange
                return None
            _key = self.get_key(keys[0])

            if self.is_list(_key):
                if key not in dic:
                    _key = len(dic[key]) if not _key else _key  # assing chang
                    dic[key] = [] # CHELOU

                if _key.isdigit():
                    _key = int(_key)
                    _len = len(dic[key])

                    if _len > _key + 1:
                        # if key is upper than length of list like  list[5] but list as only 3 item
                        # raise a parse Error
                        raise UnknowKey

                    if _key == _len:
                        # if not element in list , create one
                        dic[key].insert(_key, None)
                    recursive(dic[key], _key, keys[1:])
                else:
                    raise UnknowKey

            elif self.is_object(_key):
                if not dic[key]:
                    dic[key] = {}
                # if _key not in dictionary[key]:
                #     dictionary[key][_key]
                recursive(dic[key], _key, keys[1:])

            else:
                raise UnknowType
        try:
            recursive(dictionary, self._split[0], self._split[1:])
        except Exception as e:
            print(e)
        return dictionary
