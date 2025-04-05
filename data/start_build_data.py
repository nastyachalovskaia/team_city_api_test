from pydantic import BaseModel


class StartBuildResponseModel(BaseModel):
    id: int
    buildTypeId: str
    state: str
    href: str
    webUrl: str

    class Config:
        extra = "ignore"

class BuildType(BaseModel):
    id: str

class StartBuildDataModel(BaseModel):
    buildType: BuildType

class StartBuildData:
    @staticmethod
    def start_build(build_id: str) -> StartBuildDataModel:

        if not build_id:
            raise ValueError("build_id не может быть пустым")

        return StartBuildDataModel(
            buildType=BuildType(id=build_id)
        )
