from typing import Any, Dict, List, Union

from pydantic import BaseModel


class Attribute(BaseModel):
    condition: Dict
    type: str
    values: Union[List, str]


class ProjectSettings(BaseModel):
    attributes: Dict[str, Attribute]
    connection_name: str
    name: str
    path: str


class Project(BaseModel):
    name: str
    connection: str
    path: str


class ImageRequest(BaseModel):
    project: str
    path: str


class AnnotationRequest(BaseModel):
    project: str
    path: str


class Region(BaseModel):
    attributes: Dict[str, Union[None, int, str]]
    points: List[float]
    shape: str


class Annotations(BaseModel):
    file_attributes: Dict = {}
    regions: List[Region] = []


class SaveAnnotationRequest(BaseModel):
    project: str
    path: str
    annotations: Annotations


class Parameter(BaseModel):
    name: str
    description: str = ""
    value: Any = None


class Connection(BaseModel):
    name: str
    storage_type: str
    params: List[Parameter]


class StorageTypes(BaseModel):
    storage_types: Dict[str, List[Parameter]] = {
        "Local": [],
        "Azure": [
            Parameter(
                name="connection_string",
                description="Connection String for the access key",
            ),
            Parameter(
                name="container_name", description="Target container on storage account"
            ),
        ],
        "S3": [
            Parameter(name="aws_access_key_id", description="Access Key ID"),
            Parameter(name="aws_secret_access_key", description="Secret Access Key"),
            Parameter(name="bucket", description="Bucket name"),
        ],
    }
