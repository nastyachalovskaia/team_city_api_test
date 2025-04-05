from api.auth_api import AuthAPI
from api.project_api import ProjectAPI
from api.user_api import UserAPI
from api.build_conf_api import BuildConfAPI
from api.start_build_api import StartBuildAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.project_api = ProjectAPI(session)
        self.user_api = UserAPI(session)
        self.build_conf_api = BuildConfAPI(session)
        self.start_build_api = StartBuildAPI(session)

    def close_session(self):
        self.session.close()