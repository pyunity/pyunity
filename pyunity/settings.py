from .logger import get_tmp
import os
import json

class LiveDict:
    def __init__(self, d, parent=None):
        self.d = {}
        for name, value in d.items():
            if isinstance(value, dict):
                self.d[name] = LiveDict(value, self)
            else:
                self.d[name] = value
        self.parent = parent

    def __getitem__(self, item):
        return self.d[str(item)]

    def __setitem__(self, item, value):
        if isinstance(value, dict):
            value = LiveDict(value)
        self.d[str(item)] = value
        if isinstance(value, LiveDict):
            value.parent = self
        self.update()

    def __delitem__(self, item):
        self.d.pop(item)
        self.update()

    def __contains__(self, item):
        return str(item) in self.d

    def __iter__(self):
        return iter(self.d)

    def update(self):
        if self.parent is not None:
            self.parent.update()

    def todict(self):
        d = {}
        for name, value in self.d.items():
            if isinstance(value, LiveDict):
                d[name] = value.todict()
            else:
                d[name] = value
        return d

    def keys(self):
        return self.todict().keys()

    def values(self):
        return self.todict().values()

    def items(self):
        return self.todict().items()

    def pop(self, item):
        if item in self:
            val = self[item]
            del self[item]
            self.update()
            return val
        raise KeyError(item)

class Database(LiveDict):
    def __init__(self, path):
        super(Database, self).__init__(json.loads(open(path).read()))
        self.path = path

    def update(self):
        with open(self.path, "w+") as f:
            f.write(json.dumps(self.todict()))

    def refresh(self):
        with open(self.path, "w+") as f:
            f.write(json.dumps(self.todict()))

file = os.path.join(os.path.dirname(get_tmp()), "settings.json")
if not os.path.isfile(file):
    with open(file, "w+") as f:
        f.write("{}")

db = Database(file)
