import time
from typing import Optional
from pydantic import BaseModel
from utils.data_generator import DataGenerator

class ProjectDataModel(BaseModel):
    parentProject: dict
    name: str
    id: str
    copyAllAssociatedSettings: bool

class ProjectData:
    @staticmethod
    def create_project_data() -> ProjectDataModel:
        return ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=f"{DataGenerator.fake_name()}_{int(time.time())}",
            id=DataGenerator.fake_project_id(),
            copyAllAssociatedSettings=True
        )

class ParentProjectModel(BaseModel):
    id: str
    name: str
    description: str
    href: str
    webUrl: str

class BuildTypes(BaseModel):
    count: int
    buildType: list = []

class Templates(BaseModel):
    count: int
    buildType: list = []

class ParametersModel(BaseModel):
    property: list = []
    count: int
    href: str

class ProjectResponseModel(BaseModel):
    id: str
    name: str
    parentProjectId: str
    virtual: bool
    description: Optional[str] = None
    href: str
    webUrl: str
    parentProject: ParentProjectModel
    buildTypes: Optional[BuildTypes] = None
    templates: Optional[Templates] = None
    deploymentDashboards: Optional[dict[str, int]] = None
    parameters: Optional[ParametersModel] = None
    vcsRoots: dict
    projectFeatures: dict
    projects: dict

    class Config:
        extra = "allow"