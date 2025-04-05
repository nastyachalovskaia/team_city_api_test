import allure
import pytest

from data.project_data import ProjectData, ProjectResponseModel


class TestProjectCreate:
    project_data = None

    @classmethod
    def setup_class(cls):
        cls.project_data = ProjectData.create_project_data()
        cls.project_data_id = cls.project_data.id

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
    @allure.title('Проверка создания проекта')
    @allure.description('Тест проверяет создание нового проекта и его появление в общем списке проектов.')
    def test_create_project(self, super_admin, created_project):
        with allure.step('Отправка запроса на создание проекта'):
            project = created_project()

        with allure.step('Проверка ответа создания проекта'):
            assert "_Root" in project.parentProjectId, "Проект должен быть создан в корне"
            assert project.id, "ID проекта не должен быть пустым"

        with allure.step('Проверка через API'):
            fetched_project = super_admin.api_manager.project_api.get_project_by_locator(project.id).text
            fetched_project = ProjectResponseModel.model_validate_json(fetched_project)
            assert fetched_project.id == project.id, f"Ожидался ID {project.id}, получен {fetched_project.id}"
