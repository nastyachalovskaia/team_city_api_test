from enums.roles import Roles


class Role:
    def __init__(self, role_id, scope="g", href=None):
        if role_id not in Roles.__members__:
            raise ValueError(f"Invalid role: {role_id}")
        self.role_id = role_id
        self.scope = scope
        self.href = href