
class QueryDimentional(dict):

    def getlist(self, key, default=None):
        if key not in self:
            return default
        return [self.get(key)]
