# Cache Handler
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def to_dict(self):
        return dict(self.cache)

    def load(self, data):
        self.cache = OrderedDict(data)


class LFUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.freq = {}
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.freq[key] += 1
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.freq[key] += 1
        else:
            if len(self.cache) >= self.capacity:
                least_used = min(self.freq, key=self.freq.get, default=None)
                if least_used:
                    del self.cache[least_used]
                    del self.freq[least_used]
            self.cache[key] = value
            self.freq[key] = 1

    def to_dict(self):
        return {'cache': self.cache, 'freq': self.freq}

    def load(self, data):
        self.cache = dict(data.get('cache', {}))
        self.freq = dict(data.get('freq', {}))

