from starburst_client.client import Client
from starburst_client.model import Role, User, Group
from starburst_client.auth import Auth


class Starburst:
    def __init__(self, base_url: str, auth: None | Auth = None) -> None:
        assert isinstance(base_url, str), base_url
        assert auth is None or isinstance(auth, Auth), auth

        self.client = Client(base_url, auth)

    def get_roles(self):
        for role in self.client.list_roles():
            yield Role(role, self.client)

    def create_role(self, name: str, description: str | None = None):
        return Role(self.client.create_role(name, description), self.client)

    def get_role(self, role_id: int):
        return Role(self.client.get_role(role_id), self.client)

    def get_user(self, username: str):
        return User(username, self.client)

    def get_group(self, group_name: str):
        return Group(group_name, self.client)
