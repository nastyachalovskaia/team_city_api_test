from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class BuildConfAPI(CustomRequester):
    def create_build(self, build_conf_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildTypes", data=build_conf_data, expected_status=expected_status)

    def delete_build(self, build_id: str):
        return self.send_request("DELETE", f"/app/rest/buildTypes/id:{build_id}",
                                 expected_status=HTTPStatus.NO_CONTENT)