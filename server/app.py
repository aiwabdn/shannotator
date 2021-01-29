import os
from datetime import datetime
from typing import Dict, List

from box import Box
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from connection import ConnectionManager
from data import (
    AnnotationRequest,
    Annotations,
    Connection,
    ImageRequest,
    Project,
    ProjectSettings,
    SaveAnnotationRequest,
    StorageTypes,
)
from project import ProjectManager

if not os.path.isdir("../storage"):
    os.makedirs("../storage")

app = FastAPI()
ConnectionManager.init()
ProjectManager.init()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/supported_storages")
def get_supported_storages():
    return StorageTypes()


@app.post("/create_connection")
def create_connection(conn: Dict):
    conn = Box(conn)
    ConnectionManager.create_connection(
        name=conn.name, storage_type=conn.storage_type, params=conn.params
    )


@app.get("/saved_connection_names", response_model=List[str])
def get_saved_connection_names():
    return ConnectionManager.get_saved_connection_names()


@app.post("/create_project")
def create_project(project: Project):
    ProjectManager.create_project(
        name=project.name, connection_name=project.connection, path=project.path
    )


@app.get("/saved_project_names", response_model=List[str])
def get_saved_project_names():
    return ProjectManager.get_saved_project_names()


@app.post("/load_project/{name}")
def load_project(name: str):
    ProjectManager.load_project(name)


@app.get("/project_files/{project_name}", response_model=List[str])
def get_project_files(project_name: str):
    return ProjectManager.get_filenames(project_name)


@app.get("/project_settings/{project_name}", response_model=ProjectSettings)
def get_project_settings(project_name: str):
    return ProjectManager.get_project_details(project_name)


@app.post("/file_request")
def fetch_file(request: ImageRequest):
    filename = ProjectManager.get_file(
        project_name=request.project, filename=request.path
    )
    return FileResponse(path=filename)


@app.post("/annotation_request", response_model=Annotations)
def fetch_annotation(request: AnnotationRequest):
    return ProjectManager.get_annotations(
        project_name=request.project, filename=request.path
    )


@app.post("/save_annotation")
def save_annotation(request: SaveAnnotationRequest):
    ProjectManager.save_annotations(
        project_name=request.project,
        filename=request.path,
        annotations=request.annotations.dict(),
    )


@app.post("/update_attributes")
def update_attributes(request: Dict):
    request = Box(request)
    ProjectManager.update_attributes(
        project_name=request.project, attributes=request.attributes
    )


@app.post("/download_project")
def download_project(request: Dict):
    request = Box(request)
    data = ProjectManager.get_project_data(project_name=request.project)
    tmpfile = f"/tmp/{request.project}_{datetime.now()}"
    if request.format == "json":
        data.to_json(filename=tmpfile)
    elif request.format == "yaml":
        data.to_yaml(filename=tmpfile)

    return FileResponse(path=tmpfile)
