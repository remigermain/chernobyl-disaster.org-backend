class QueryDimentionalNested(dict):
    def getlist(self, key, default=None):
        print(f"--------{key}------------")
        if key not in self:
            return default
        val = super().get(key)
        return val if isinstance(val, list) else [val]

    def get(self, key, default=None):
        if key not in self:
            return default
        val = super().get(key)
        if isinstance(val, list):
            return val
        return val
