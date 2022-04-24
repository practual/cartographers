import json


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)


def loads(*args, **kwargs):
    return json.loads(*args, **kwargs)


def dumps(*args, **kwargs):
    return json.dumps(*args, cls=JsonEncoder, **kwargs)
