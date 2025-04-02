import allure
import pytest

from data.project_data import ProjectData, ProjectResponseModel

class TestProjectCreate:
    project_data = None

    @classmethod
    def setup_class(cls):
        cls.project_data= ProjectData.create_project_data()
        cls.project_data_id = cls.project_data.id

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
    @allure.title('Проверка создания проекта')
    @allure.description('Тест проверяет создание нового проекта и его появление в общем списке проектов.')
    def test_create_project(self, super_admin, project_data):
        project_data_1 = project_data()
        with allure.step('Отправка запроса на создание проекта'):
            response = super_admin.api_manager.project_api.create_project(project_data_1.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert project_response.id == project_data_1.id
        with pytest.assume:
            assert project_response.parentProjectId == project_data_1.parentProject["locator"]
        with allure.step("отправка запроса на получение информации о созданном проекте"):
            response = super_admin.api_manager.project_api.get_project_by_locator(project_data_1.name).text
        with allure.step("проверка соответствия параметров созданного проекта с отправленными данными"):
            created_project = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert created_project.id == project_data_1.id, \
                f"expected project id= {project_data_1.id}, but '{created_project.id}' given"

    # @allure.feature("Управление build'ом")
    # @allure.story('Создание build config')
    # @allure.title('Проверка создания build config')
    # @allure.description('Тест проверяет создание нового build config и его появление в общем списке build config.')
    # def test_create_build_config(self):


