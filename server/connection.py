import os
from glob import glob
from tempfile import NamedTemporaryFile
from typing import Dict, List, Optional, Union

import boto3
from box import Box

from storage_clients import AzureStorageClient


class BaseConnection:
    def __init__(self, name: str = "", params: Union[Box, Dict] = {}):
        self.name = name
        self.params = Box(params)

    def get_file(self, path: str) -> str:
        raise NotImplementedError

    def get_filenames(
        self, extensions: Optional[List[str]] = ["png", "jpg", "jpeg", "bmp"]
    ) -> List[str]:
        raise NotImplementedError


class LocalConnection(BaseConnection):
    STORAGE_TYPE = "Local"

    def __init__(self, name: str = "", params: Union[Box, Dict] = {}):
        super().__init__(name, params)

    def get_file(self, path: str) -> str:
        if os.path.isfile(path):
            return path
        return None

    def get_filenames(
        self, path: str, extensions: Optional[List[str]] = ["png", "jpg", "jpeg", "bmp"]
    ) -> List[str]:
        extensions = extensions + [_.upper() for _ in extensions]
        filenames = []
        for extension in extensions:
            foundfiles = glob(f"{path}/**/*.{extension}", recursive=True)
            filenames.extend(foundfiles)

        return filenames


class S3Connection(BaseConnection):
    STORAGE_TYPE = "S3"

    def __init__(self, name: str = "", params: Union[Box, Dict] = {}):
        super().__init__(name, params)
        self.client = boto3.client(
            "s3",
            aws_access_key_id=params.aws_access_key_id,
            aws_secret_access_key=params.aws_secret_access_key,
        )
        self.bucket = params.bucket
        self.cache = {}

    def get_file(self, path: str) -> str:
        if path in self.cache:
            return self.cache[path].name

        if len(self.cache) == 5:
            removing = list(self.cache.keys())[0]
            self.cache[removing].close()
            del self.cache[removing]

        tmpfile = NamedTemporaryFile()
        self.client.download_file(self.bucket, path, tmpfile.name)
        self.cache[path] = tmpfile

        return tmpfile.name

    def get_filenames(
        self, path: str, extensions: Optional[List[str]] = ["png", "jpg", "jpeg", "bmp"]
    ) -> List[str]:
        extensions = set(extensions + [_.upper() for _ in extensions])
        all_files = [
            e["Key"]
            for p in self.client.get_paginator("list_objects_v2").paginate(
                Bucket=self.bucket, Prefix=path
            )
            for e in p["Contents"]
        ]
        found_files = list(filter(lambda l: l.split(".")[-1] in extensions, all_files))
        return found_files


class AzureConnection(BaseConnection):
    STORAGE_TYPE = "Azure"

    def __init__(self, name: str = "", params: Union[Box, Dict] = {}):
        super().__init__(name, params)
        self.azure = AzureStorageClient(**self.params)
        self.cache = {}

    def get_file(self, path: str) -> str:
        if path in self.cache:
            return self.cache[path].name

        if len(self.cache) == 5:
            removing = list(self.cache.keys())[0]
            self.cache[removing].close()
            del self.cache[removing]

        tmpfile = NamedTemporaryFile()
        self.azure.download(path, tmpfile.name)
        self.cache[path] = tmpfile

        return tmpfile.name

    def get_filenames(
        self, path: str, extensions: Optional[List[str]] = ["png", "jpg", "jpeg", "bmp"]
    ) -> List[str]:
        extensions = set(extensions + [_.upper() for _ in extensions])
        all_files = self.azure.ls_files(path, recursive=True)
        found_files = list(filter(lambda l: l.split(".")[-1] in extensions, all_files))
        return found_files


class ConnectionManager:
    REGISTERED_STORAGES = [LocalConnection, AzureConnection, S3Connection]
    SAVE_PATH = "../storage/connections.yaml"
    CURRENT_CONNECTIONS = {}

    @classmethod
    def init(cls):
        if not os.path.isfile(cls.SAVE_PATH):
            with open(cls.SAVE_PATH, "a") as f:
                f.write("all_connections: []\n")

    @classmethod
    def get_supported_storages(cls) -> List[str]:
        return [_.STORAGE_TYPE for _ in cls.REGISTERED_STORAGES]

    @classmethod
    def get_storage_class(cls, storage_type: str) -> BaseConnection:
        for storage in cls.REGISTERED_STORAGES:
            if storage.STORAGE_TYPE == storage_type:
                return storage

    @classmethod
    def get_connection_details(cls, name: str) -> Union[Box, Dict]:
        existing = Box.from_yaml(filename=cls.SAVE_PATH)
        return existing[name]

    @classmethod
    def get_saved_connection_names(cls) -> List[str]:
        existing = Box.from_yaml(filename=cls.SAVE_PATH)
        return existing.all_connections

    @classmethod
    def create_connection(cls, name: str, storage_type: str, params: Union[Box, Dict]):
        existing = Box.from_yaml(filename=cls.SAVE_PATH)
        if name in existing:
            raise NameError(f"Provided connection name {name} is already registered")
        existing[name] = {"name": name, "storage_type": storage_type, "params": params}
        existing.all_connections.append(name)
        existing.to_yaml(filename=cls.SAVE_PATH)

    @classmethod
    def open_connection(cls, name: str):
        if name not in cls.CURRENT_CONNECTIONS:
            details = cls.get_connection_details(name)
            storage_class = cls.get_storage_class(details.storage_type)
            cls.CURRENT_CONNECTIONS[name] = storage_class(name, details.params)

    @classmethod
    def get_file(cls, connection_name: str, path: str):
        return cls.CURRENT_CONNECTIONS[connection_name].get_file(path)

    @classmethod
    def get_filenames(
        cls,
        connection_name: str,
        path: str,
        extensions: Optional[List[str]] = ["png", "jpg", "jpeg", "bmp"],
    ) -> List[str]:
        return cls.CURRENT_CONNECTIONS[connection_name].get_filenames(path, extensions)
