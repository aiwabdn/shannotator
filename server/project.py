import os
from typing import Dict, List, Optional, Tuple, Union

from box import Box

from connection import ConnectionManager


class Project:
    SAVE_PATH = "../storage"

    def __init__(
        self,
        name: str,
        connection_name: str,
        path: str,
        attributes: Optional[Dict] = {},
    ):
        self.name = name
        self.connection_name = connection_name
        self.path = path
        self.attributes = attributes
        self.project_files = []
        self.annotations = {}
        self.annotation_filepath = f"{self.SAVE_PATH}/annotations_{self.name}.yaml"
        self.open_connection()

    def open_connection(self):
        ConnectionManager.open_connection(self.connection_name)

    def get_filenames(
        self, extensions: Optional[List[str]] = ["png", "jpg", "jpeg", "bmp"]
    ):
        if len(self.project_files) == 0:
            return ConnectionManager.get_filenames(
                self.connection_name, self.path, extensions
            )
        return self.project_files

    def get_file(self, path: str):
        filepath = ConnectionManager.get_file(self.connection_name, path)
        anns = self.annotations.get(path, {})
        return filepath, anns

    def save_annotations(self, filename: str, annotations: Dict):
        self.annotations[filename] = annotations
        Box(self.annotations).to_yaml(filename=self.annotation_filepath)

    def load_annotations(self):
        if not os.path.isfile(self.annotation_filepath):
            with open(self.annotation_filepath, "a") as f:
                f.write(f"name: {self.name}\n")

        self.annotations = Box.from_yaml(filename=self.annotation_filepath)

    def update_attributes(self, attributes: Dict):
        self.attributes = attributes


class ProjectManager:
    SAVE_PATH = "../storage/projects.yaml"
    CURRENT_PROJECTS = {}

    @classmethod
    def init(cls):
        if not os.path.isfile(cls.SAVE_PATH):
            with open(cls.SAVE_PATH, "a") as f:
                f.write("all_projects: []\n")

    @classmethod
    def get_project_details(cls, name: str) -> Union[Box, Dict]:
        existing = Box.from_yaml(filename=cls.SAVE_PATH)
        return existing[name]

    @classmethod
    def get_saved_project_names(cls) -> List[str]:
        existing = Box.from_yaml(filename=cls.SAVE_PATH)
        return existing.all_projects

    @classmethod
    def create_project(cls, name: str, connection_name: str, path: str):
        existing = Box.from_yaml(filename=cls.SAVE_PATH)
        if name in existing:
            raise NameError(f"Provided project name {name} is already registered")
        existing[name] = {
            "name": name,
            "connection_name": connection_name,
            "path": path,
            "attributes": {},
        }
        existing.all_projects.append(name)
        existing.to_yaml(filename=cls.SAVE_PATH)

    @classmethod
    def load_project(cls, name: str):
        if name not in cls.CURRENT_PROJECTS:
            existing = cls.get_project_details(name)
            cls.CURRENT_PROJECTS[name] = Project(**existing)
            cls.CURRENT_PROJECTS[name].load_annotations()

    @classmethod
    def get_file(cls, project_name: str, filename: str) -> Tuple[str, Dict]:
        return cls.CURRENT_PROJECTS[project_name].get_file(filename)

    @classmethod
    def get_filenames(cls, project_name: str) -> List[str]:
        return cls.CURRENT_PROJECTS[project_name].get_filenames()

    @classmethod
    def update_attributes(cls, project_name: str, attributes: Union[Box, Dict]):
        cls.CURRENT_PROJECTS[project_name].update_attributes(attributes)
        existing = Box.from_yaml(filename=cls.SAVE_PATH)
        existing[project_name].attributes = attributes
        # TODO: handle concurrency in file write
        existing.to_yaml(filename=cls.SAVE_PATH)

    @classmethod
    def save_annotations(
        cls, project_name: str, filename: str, annotations: Union[Box, Dict]
    ):
        cls.CURRENT_PROJECTS[project_name].save_annotations(filename, annotations)

    @classmethod
    def get_project_data(cls, project_name: str):
        data = Box()
        data["details"] = cls.get_project_details(project_name)
        data["annotations"] = cls.CURRENT_PROJECTS[project_name].annotations
        _ = data["annotations"].pop("name")
        return data
