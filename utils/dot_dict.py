class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = DotDict(value)
        elif isinstance(value, list | tuple):
            value = list(map(lambda x:  DotDict(x) if isinstance(x, dict) else x, value))
        return value
