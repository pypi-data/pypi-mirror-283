import json
import os
from typing import Optional, Type, TypeVar

from credio.util.type import Object


V = TypeVar("V")


class Store(dict):
    def __init__(self):
        pass

    def get(self, key: str, type: Type[V] = str) -> Optional[V]:
        if key in self.keys():
            return self[key]

    def load(self, *keys: str):
        for key in keys:
            self[key] = os.environ[key]
        return self

    def load_json(self, obj: dict):
        for key in obj:
            self[key] = str(obj[key])
        return self

    def load_all(self):
        return self.load(*os.environ.keys())

    def load_file(self, path: Optional[str]):
        if path is None or not os.path.isfile(path):
            return self
        with open(path, "rb") as file:
            json_obj = Object(json.loads(file.read().decode()))
            return self.load_json(json_obj)


default = Store().load_all()
"""Default Configuration Store."""
