# Codes: https://www.loc.gov/standards/iso639-2/php/code_list.php

import json
from pathlib import Path

directory = Path(__file__).resolve().parent / "locale"

def field(name, fields):
    def __repr__(self):
        parts = []
        for field in self._fields_:
            parts.append(f"{field}={getattr(self, field)!r}")
        return "field(" + ", ".join(parts) + ")"

    ns = {"__repr__": __repr__}
    for x in fields:
        ns[x] = None
    t = type(name, (object,), ns)
    t._fields_ = fields
    return t

class Locale:
    def __init__(self, code):
        with open(directory / (code + ".json"), encoding="utf-8") as f:
            self.mapping = json.load(f)

        self.name = self.mapping.pop("name")
        self.set(self, self.mapping)

    def __repr__(self):
        parts = []
        for field in self.mapping:
            parts.append(f"{field}={getattr(self, field)!r}")
        return "Locale(" + ", ".join(parts) + ")"

    def set(self, obj, d):
        for key in d:
            if isinstance(d[key], dict):
                nt = field(key, list(d[key].keys()))
                new = nt()
                setattr(obj, key, new)
                self.set(new, d[key])
            else:
                setattr(obj, key, d[key])

locale = Locale("en_GB")
