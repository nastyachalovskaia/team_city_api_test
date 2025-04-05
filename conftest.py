import json
import time

import pytest
import requests

from api.api_manager import ApiManager
from data.build_config_data import BuildConfigData, BuildResponseModel
from data.project_data import ProjectData, ProjectResponseModel
from data.user_data import UserData
from entities.role import Role
from entities.user import User
from resources.user_creds import SuperAdminCreds


@pytest.fixture(scope="session")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope="session")
def super_admin(user_session, super_admin_creds):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, new_session, ["SUPER_ADMIN"])
    super_admin.api_manager.auth_api.auth_and_get_csrf(super_admin.creds)
    return super_admin

@pytest.fixture(scope="session")
def super_admin_creds():
    return SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD

@pytest.fixture
def user_create(user_session, super_admin):
    created_users_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, scope="g")
        super_admin.api_manager.user_api.create_user(user_data)
        new_session = user_session()
        created_users_pool.append(user_data['username'])
        return User(user_data['username'], user_data['password'], new_session, [Role(role)])

    yield _user_create

    for username in created_users_pool:
        super_admin.api_manager.user_api.delete_user(username)

PROJECT_IDS_TO_DELETE = []
BUILD_IDS_TO_DELETE = []

@pytest.fixture(scope="session")
def created_project(super_admin):
    created_projects = []

    def _created_project():
        project = ProjectData.create_project_data()

        print(f"\nСоздаю проект: {project.id}")
        response = super_admin.api_manager.project_api.create_project(project.model_dump())

        created_project = ProjectResponseModel.model_validate_json(response.text)
        created_projects.append(created_project.id)
        PROJECT_IDS_TO_DELETE.append(created_project.id)

        print(f"Создан проект ID: {created_project.id}")

        return created_project

    yield _created_project

@pytest.fixture
def build_config_data(super_admin):

    def _build_config_data(project_id: str):
        build = BuildConfigData.build_config_data(project_id)
        response = super_admin.api_manager.build_conf_api.create_build(build.model_dump())
        created_build = BuildResponseModel.model_validate_json(response.text)
        BUILD_IDS_TO_DELETE.append(created_build.id)

        return created_build

    yield _build_config_data

    for build_id in BUILD_IDS_TO_DELETE:
        try:
            super_admin.api_manager.build_conf_api.delete_build(build_id)
        except Exception as e:
            print(f"Ошибка при удалении билда {build_id}: {e}")
    for id_project in PROJECT_IDS_TO_DELETE:
        try:
            super_admin.api_manager.project_api.clean_up_project(id_project)
        except Exception as e:
            print(f"Ошибка при удалении проекта {id_project}: {e}")