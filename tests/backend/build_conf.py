import allure
import pytest


class TestBuildConf:
    build_data = None

    @allure.feature("Управление build'ом")
    @allure.story('Создание build config')
    @allure.title('Проверка создания build config')
    @allure.description('Тест проверяет создание нового build config и его появление в общем списке build config.')
    def test_create_build_config(self, super_admin, build_config_data, created_project):
        with allure.step('Отправка запроса на создание проекта (для изолированного теста)'):
            project = created_project()

        with allure.step('Отправка запроса на наличие проекта'):
            project_info = super_admin.api_manager.project_api.get_project(project.id).json()
        with pytest.assume:
            assert project_info['id'] == project.id, "Проект не найден в TeamCity!"

        with allure.step('Отправка запроса на создание билда'):
            build_config = build_config_data(project.id)

        with pytest.assume:
            assert build_config.project.id == project.id, (
                f"Билд привязан к другому проекту! "
                f"Ожидался: {project.id}, получен: {build_config.project.id}"
            )

        with pytest.assume:
            assert build_config.project.id == project.id
            assert project.id in build_config.id

