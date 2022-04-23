import json
from pymemcache import Client


class JsonSerializer:
    def serialize(self, key, value):
        if isinstance(value, str):
            return value.encode('utf-8'), 1
        return json.dumps(value).encode('utf-8'), 2

    def deserialize(self, key, value, flag):
        if flag == 1:
            return value.decode('utf-8')
        return json.loads(value.decode('utf-8'))


cache = Client(('localhost', 11211), serde=JsonSerializer())
