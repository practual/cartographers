import json

from flask import current_app as app
from flask import g
from pymemcache import Client

from serializer import JsonEncoder


class JsonSerializer:
    def serialize(self, key, value):
        if isinstance(value, str):
            return value.encode('utf-8'), 1
        return json.dumps(value, cls=JsonEncoder).encode('utf-8'), 2

    def deserialize(self, key, value, flag):
        if flag == 1:
            return value.decode('utf-8')
        return json.loads(value.decode('utf-8'))


def get_cache():
    if 'cache' not in g:
        g.cache = Client((app.config['MEMCACHE']['HOST'], 11211), serde=JsonSerializer())
    return g.cache
