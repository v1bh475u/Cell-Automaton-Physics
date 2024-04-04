import json

class HashTable:
    def __init__(self):
        self.hashes = {}

    def set(self, key, value):
        self.hashes[json.dumps(key)] = value

    def get(self, key):
        return self.hashes.get(json.dumps(key))

    def has(self, key):
        return json.dumps(key) in self.hashes

    def delete(self, key):
        del self.hashes[json.dumps(key)]

    def each(self, func, early_return=False):
        for key in self.hashes:
            value = self.hashes[key]
            if early_return:
                result = func(key, value)
                if result:
                    return result
            else:
                func(key, value)
