from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class StartBuildAPI(CustomRequester):

    def start_build(self, build_conf_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildQueue", data=build_conf_data, expected_status=expected_status)

    def get_build(self, build_id: int):
        return self.send_request("GET",f"/app/rest/builds/id:{build_id}",
                                     expected_status=HTTPStatus.OK
                                     )