import os

from credio.util.type import lazy

from .store import default as store


class File:
    @staticmethod
    def _mkdir(path: str):
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.isdir(path):
            raise Exception("Path '%s' is not a directory" % path)

    def __init__(self):
        storage_path = store.get("STORAGE_PATH") or "/tmp/credio"
        File._mkdir(storage_path)
        self.storage_path = storage_path

    def path(self, bucket: str, *folders: str, name: str) -> str:
        folder_path = os.path.join(self.storage_path, bucket, *folders)
        File._mkdir(folder_path)
        return os.path.join(folder_path, name)

    def store(self, bucket: str, *folders: str, name: str, data: bytes) -> str:
        file_path = self.path(bucket, *folders, name=name)
        with open(file_path, "+wb") as file:
            file.write(data)
        return file_path

    def retrieve(self, bucket: str, *folders: str, name: str) -> bytes:
        file_path = os.path.join(self.storage_path, bucket, *folders, name)
        with open(file_path, "+rb") as file:
            return file.read()


default = lazy(File)
"""Simple storage."""
