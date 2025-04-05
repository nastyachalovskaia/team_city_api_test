from api.api_manager import ApiManager


class User:
    def __init__(self, username: str, password: str, session: ApiManager, roles: list, **kwargs):
        self.username = username
        self.password = password
        self.email = None
        self.roles = roles
        self.groups = None
        self.api_manager = session

    @property # превращает метод creds в атрибут только для чтения
    def creds(self):
        return self.username, self.password