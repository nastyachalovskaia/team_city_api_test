import allure
import pytest


class TestStartBuildConf:
    build_data = None

    @allure.feature("Управление run build'a")
    @allure.story('Создание run build config')
    @allure.title('Проверка создания run build config')
    @allure.description('Тест проверяет запуск нового build config.')
    def test_start_build_config(self, super_admin, build_config_data, created_project, start_build):
        with allure.step('Создание проекта'):
            project = created_project()

        with allure.step('Создание билд-конфигурации'):
            build_config = build_config_data(project.id)
        with allure.step('Запуск билда с ожиданием (для изолированного теста)'):
            build_response = start_build(build_config.id)
        with pytest.assume:
            assert build_response.id, "Билд не был запущен"
        with pytest.assume:
            assert build_response.state in ('queued', 'running'), f"Неожиданный статус билда: {build_response.state}"
        with pytest.assume:
            assert build_response.href, "Нет ссылки на билд"
