from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester


class ProjectAPI(CustomRequester):

    def create_project(self, project_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/projects", data=project_data, expected_status=expected_status)

    def get_project(self, project_id: str):
        """Получает проект по ID"""
        return self.send_request("GET",f"/app/rest/projects/id:{project_id}",
            expected_status=200
        )
    def delete_project(self, project_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/projects/id:{project_id}", expected_status=expected_status)

    def clean_up_project(self, created_project_id):
        self.delete_project(created_project_id)
        get_projects_response = self.get_project(created_project_id).json()
        project_ids = [project.get('id', {}) for project in get_projects_response.get('project', [])]
        assert created_project_id not in project_ids, "ID созданного проекта найден в списке проектов после удаления."

    def get_project_by_locator(self, locator):
        return self.send_request("GET", f"/app/rest/projects/{locator}")