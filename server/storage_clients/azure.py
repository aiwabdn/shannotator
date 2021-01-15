import os
from pathlib import Path
from typing import Union

from box import Box

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient


class AzureStorageClient:
    """
    Azure storage account manager class.

    Connects to `container_name` using Azure storage account information
    provided in `yaml` format at `config_path`. For sample, refer to
    `sample_configs/azure_storage_config.yaml`.

    Creates the container if it does not exist. Wraps methods useful for
    uploading, downloading directories/files to and from Azure container.
    Can also list and delete files in container.
    """
    def __init__(self, connection_string: str, container_name: str):
        self.client = self.__get_container_client(connection_string,
                                                  container_name)

    def __get_container_client(self, connection_string: str,
                               container_name: str):
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string)
        try:
            container_client = blob_service_client.create_container(
                container_name)
            print(f'Container {container_name} created')
        except ResourceExistsError:
            container_client = blob_service_client.get_container_client(
                container_name)
        return container_client

    def upload(self,
               source: Union[str, Path],
               dest: Union[str, Path],
               overwrite: bool = False):
        """
        Upload a file or directory to a path inside the container
        """
        source = str(source)
        dest = str(dest)
        if (os.path.isdir(source)):
            self.upload_dir(source, dest, overwrite)
        else:
            self.upload_file(source, dest, overwrite)

    def upload_file(self,
                    source: Union[str, Path],
                    dest: Union[str, Path],
                    overwrite: bool = False):
        """
        Upload a single file to a path inside the container
        """
        # Upload
        source = str(source)
        dest = str(dest)
        print(f'Uploading {source} to {dest}')
        with open(source, 'rb') as data:
            try:
                self.client.upload_blob(name=dest,
                                        data=data,
                                        overwrite=overwrite)
            except ResourceExistsError:
                print('Blob exists')

    def copy_file(self,
                  source: Union[str, Path],
                  dest: Union[str, Path],
                  overwrite: bool = False):
        """
        Copy blob from one path in container to another.
        """
        source = str(source)
        dest = str(dest)
        if not self.file_exists(source):
            raise FileNotFoundError(f'{source} does not exist')
        sc = self.client.get_blob_client(source)
        dc = self.client.get_blob_client(dest)
        if self.file_exists(dest) and (not overwrite):
            print(f'{dest} exists and overwrite is False')
        else:
            status = dc.start_copy_from_url(sc.url)
            if status['copy_status'] == 'success':
                print(f'Copied {source} to {dest}')
            else:
                print('Copy failed')

    def move_file(self,
                  source: Union[str, Path],
                  dest: Union[str, Path],
                  overwrite: bool = False):
        """
        Move blob from one path in container to another
        """
        source = str(source)
        dest = str(dest)
        self.copy_file(source, dest, overwrite)
        self.client.delete_blob(source)

    def upload_dir(self,
                   source: Union[str, Path],
                   dest: Union[str, Path],
                   overwrite: bool = False):
        """
        Upload a directory to a path inside the container
        """
        source = str(source)
        dest = str(dest)
        prefix = '' if dest == '' else dest + '/'
        prefix += os.path.basename(source) + '/'
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = '' if dir_part == '.' else dir_part + '/'
                file_path = os.path.join(root, name)
                blob_path = prefix + dir_part + name
                self.upload_file(file_path, blob_path, overwrite)

    def download(self, source: Union[str, Path], dest: Union[str, Path]):
        """
        Download a file or directory to a path on the local filesystem
        """
        source = str(source)
        dest = str(dest)
        if not dest:
            raise Exception('A destination must be provided')

        blobs = self.ls_files(source, recursive=True)
        if blobs:
            # if source is a directory, dest must also be a directory
            if not source == '' and not source.endswith('/'):
                source += '/'
            if not dest.endswith('/'):
                dest += '/'
            # append the directory name from source to the destination
            dest += os.path.basename(os.path.normpath(source)) + '/'

            blobs = [source + blob for blob in blobs]
            for blob in blobs:
                blob_dest = dest + os.path.relpath(blob, source)
                self.download_file(blob, blob_dest)
        else:
            self.download_file(source, dest)

    def download_file(self, source: Union[str, Path], dest: Union[str, Path]):
        """
        Download a single file to a path on the local filesystem
        """
        # dest is a directory if ending with '/' or '.', otherwise it's a file
        source = str(source)
        dest = str(dest)
        if dest.endswith('.'):
            dest += '/'
        blob_dest = dest + os.path.basename(source) if dest.endswith(
            '/') else dest

        print(f'Downloading {source} to {blob_dest}')
        os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
        bc = self.client.get_blob_client(blob=source)
        with open(blob_dest, 'wb') as file:
            data = bc.download_blob()
            file.write(data.readall())

    def file_exists(self, file_path: Union[str, Path]):
        """
        Check if file exists in azure
        """
        file_path = str(file_path)
        bc = self.client.get_blob_client(file_path)
        try:
            bc.get_blob_properties()
        except ResourceNotFoundError:
            return False
        return True

    def ls_files(self, path: Union[str, Path], recursive: bool = False):
        """
        List files under a path, optionally recursively
        """
        path = str(path)
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or '/' not in relative_path:
                files.append(relative_path)
        return files

    def ls_dirs(self, path: Union[str, Path], recursive: bool = False):
        """
        List directories under a path, optionally recursively
        """
        path = str(path)
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        dirs = []
        for blob in blob_iter:
            relative_dir = os.path.dirname(os.path.relpath(blob.name, path))
            if relative_dir and (recursive or '/' not in relative_dir
                                 ) and relative_dir not in dirs:
                dirs.append(relative_dir)

        return dirs

    def rm(self, path: Union[str, Path], recursive: bool = False):
        """
        Remove a single file, or remove a path recursively
        """
        path = str(path)
        if recursive:
            self.rmdir(path)
        else:
            print(f'Deleting {path}')
            self.client.delete_blob(path)

    def rmdir(self, path: Union[str, Path]):
        """
        Remove a directory and its contents recursively
        """
        path = str(path)
        blobs = self.ls_files(path, recursive=True)
        if not blobs:
            return

        if not path == '' and not path.endswith('/'):
            path += '/'
        blobs = [path + blob for blob in blobs]
        print(f'Deleting {", ".join(blobs)}')
        self.client.delete_blobs(*blobs)
