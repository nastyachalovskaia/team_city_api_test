import time
import uuid
from typing import List
from pydantic import BaseModel
from utils.data_generator import DataGenerator


class Project(BaseModel):
    id: str

class Property(BaseModel):
    name: str
    value: str


class StepProperties(BaseModel):
    property: List[Property]


class Step(BaseModel):
    name: str
    type: str
    properties: StepProperties


class Steps(BaseModel):
    step: List[Step]


class BuildResponseModel(BaseModel):
    id: str
    name: str
    project: Project
    steps: Steps


class BuildConfigData:
    @staticmethod
    def build_config_data(project_id: str) -> BuildResponseModel:
        unique_id = f"{project_id}_Build_{int(time.time())}"

        if not project_id:
            raise ValueError("project_id не может быть пустым")

        return BuildResponseModel(
            name=DataGenerator.fake_name(),
            id=unique_id,
            project=Project(id=project_id),
            steps=Steps(
                step=[
                    Step(
                        name="myCommandLineStep",
                        type="simpleRunner",
                        properties=StepProperties(
                            property=[
                                Property(
                                    name="script.content",
                                    value="echo 'Hello World!'"
                                ),
                                Property(
                                    name="teamcity.step.mode",
                                    value="default"
                                ),
                                Property(
                                    name="use.custom.script",
                                    value="true"
                                )
                            ]
                        )
                    )
                ]
            )
        )
