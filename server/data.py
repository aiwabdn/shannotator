from typing import Any, Dict, List

from pydantic import BaseModel


class StringListResponse(BaseModel):
    data: List[str]


class Project(BaseModel):
    name: str
    connection: str
    path: str


class ProjectNames(BaseModel):
    names: List[str]


class ProjectFiles(BaseModel):
    files: List[str]


class ProjectSettings(BaseModel):
    settings: Dict


class ImageRequest(BaseModel):
    project: str
    path: str


class AnnotationRequest(BaseModel):
    project: str
    path: str


class AnnotationResponse(BaseModel):
    annotations: Dict


class SaveAnnotationRequest(BaseModel):
    project: str
    path: str
    annotations: Dict


class Parameter(BaseModel):
    name: str
    description: str = ''
    value: Any = None


class Connection(BaseModel):
    name: str
    storage_type: str
    params: List[Parameter]


class StorageTypes(BaseModel):
    storage_types: Dict[str, List[Parameter]] = {
        'Local': [],
        'Azure': [
            # Parameter(name='account_name',
            #           description='Name of storage account'),
            # Parameter(name='key', description='One of the two access keys'),
            Parameter(name='connection_string',
                      description='Connection String for the access key'),
            Parameter(name='container_name',
                      description='Target container on storage account')
        ],
        'S3': [
            Parameter(name='aws_access_key_id', description='Access Key ID'),
            Parameter(name='aws_secret_access_key',
                      description='Secret Access Key'),
            Parameter(name='bucket', description='Bucket name')
        ]
    }
