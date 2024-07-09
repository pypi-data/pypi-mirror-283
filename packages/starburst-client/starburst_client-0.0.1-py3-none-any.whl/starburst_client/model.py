import typing

from starburst_client.starburst import Client


class Role:
    def __init__(self, attributes, client: Client):
        self._id = attributes["id"]
        self._name = attributes["name"]
        self._description = attributes.get("description", None)
        self._client = client

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._client.update_role(self.id, name, self.description)
        self._name = name

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._client.update_role(self.id, self.name, description)
        self._description = description

    def __repr__(self) -> str:
        return '{}(id={}, name="{}", description="{}")'.format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.description,
        )

    def __str__(self) -> str:
        return repr(self)

    def delete(self):
        self._client.delete_role(self.id)

    def get_grants(self) -> typing.Generator["Grant", None, None]:
        for grant in self._client.list_grants(self.id):
            grant["roleId"] = self.id
            yield Grant(grant, self._client)

    def get_assignments(self) -> typing.Generator["RoleAssignment", None, None]:
        """get all subjects assigned to the current role"""
        for role_assignment in self._client.list_role_assignments(self.id):
            role_assignment["roleId"] = self.id
            yield RoleAssignment(role_assignment, self._client)

    def create_group_assignment(
        self, group_name: str, role_admin: bool = False
    ) -> "RoleAssignment":
        role_assignment = self._client.create_role_assignment_for_group(
            group_name, self.id, role_admin
        )
        role_assignment["subject"] = {"type": "GROUP", "groupName": group_name}
        return role_assignment

    def create_role_assignment(
        self, subject_role: "Role", role_admin: bool = False
    ) -> "RoleAssignment":
        role_assignment = self._client.create_role_assignment_for_role(
            subject_role.id, self.id, role_admin
        )
        role_assignment["subject"] = {"type": "ROLE", "roleId": subject_role.id}
        return role_assignment

    def create_user_assignment(
        self, username: str, role_admin: bool = False
    ) -> "RoleAssignment":
        role_assignment = self._client.create_role_assignment_for_user(
            username, self.id, role_admin
        )
        role_assignment["subject"] = {"type": "USER", "username": username}
        return RoleAssignment(role_assignment, self._client)

    def get_role_assignments(self) -> typing.Generator["RoleAssignment", None, None]:
        """get all assignments that is subject to this role itself"""
        for role_assignment in self._client.get_role_assignments_for_role(self.id):
            role_assignment["subject"] = {"type": "ROLE", "roleId": self.id}
            yield RoleAssignment(role_assignment, self._client)


class User:
    @property
    def username(self) -> str:
        return self._username

    def __init__(self, username: str, client: Client):
        self._username = username
        self._client = client

    def __repr__(self) -> str:
        return '{}(username="{}")'.format(
            self.__class__.__name__,
            self.username,
        )

    def __str__(self) -> str:
        return repr(self)

    def get_role_assignments(self) -> typing.Generator["RoleAssignment", None, None]:
        for role_assignment in self._client.get_role_assignments_for_user(
            self.username
        ):
            role_assignment["subject"] = {"type": "USER", "username": self.username}
            yield RoleAssignment(role_assignment, self._client)


class Group:
    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str, client: Client):
        self._name = name
        self._client = client

    def __repr__(self) -> str:
        return '{}(name="{}")'.format(
            self.__class__.__name__,
            self.name,
        )

    def __str__(self) -> str:
        return repr(self)

    def get_role_assignments(self) -> typing.Generator["RoleAssignment", None, None]:
        for role_assignment in self._client.get_role_assignments_for_group(self.name):
            role_assignment["subject"] = {"type": "GROUP", "groupName": self.name}
            yield RoleAssignment(role_assignment, self._client)


class RoleAssignment:
    @property
    def id(self) -> int:
        return self._id

    @property
    def subject(self) -> Group | Role | User | None:
        return self._subject

    @property
    def role_admin(self) -> bool:
        return self._role_admin

    @property
    def role_id(self) -> int:
        return self._role_id

    def __init__(self, attributes, client: Client):
        self._id = attributes["id"]
        self._role_admin = attributes["roleAdmin"]

        self._subject: Group | Role | User | None = None
        if attributes["subject"]["type"] == "USER":
            self._subject = User(attributes["subject"]["username"], client)
        elif attributes["subject"]["type"] == "GROUP":
            self._subject = Group(attributes["subject"]["groupName"], client)
        elif attributes["subject"]["type"] == "ROLE":
            role_attributes = client.get_role(attributes["subject"]["roleId"])
            self._subject = Role(role_attributes, client)

        self._role_id = attributes["roleId"]
        self._client = client

    def __repr__(self) -> str:
        return "{}(id={}, subject={}, role_admin={})".format(
            self.__class__.__name__,
            self.id,
            self.subject,
            self.role_admin,
        )

    def __str__(self) -> str:
        return repr(self)

    def get_role(self):
        return Role(self._client.get_role(self.role_id), self._client)

    def delete(self):
        if type(self.subject) is Group:
            self._client.delete_role_assignment_from_group(self.subject.name, self.id)
        elif type(self.subject) is Role:
            self._client.delete_role_assignment_from_role(self.subject.id, self.id)
        elif type(self.subject) is User:
            self._client.delete_role_assignment_from_user(
                self.subject.username, self.id
            )


class Grant:
    @property
    def id(self) -> int:
        return self._id

    @property
    def effect(self) -> str:
        return self._effect

    @property
    def action(self) -> int:
        return self._action

    @property
    def entity(self) -> dict:
        return self._entity

    @property
    def role_id(self) -> int:
        return self._role_id

    def __init__(self, attributes, client: Client):
        self._id = attributes["id"]
        self._effect = attributes["effect"]
        self._action = attributes["action"]
        self._entity = attributes["entity"]
        self._role_id = attributes["roleId"]
        self._client = client

    def __repr__(self) -> str:
        return '{}(id={}, effect="{}", action="{}", entity={}, role_id={})'.format(
            self.__class__.__name__,
            self.id,
            self.effect,
            self.action,
            self.entity,
            self.role_id,
        )

    def __str__(self) -> str:
        return repr(self)

    def get_role(self):
        return Role(self._client.get_role(self.role_id), self._client)

    def delete(self):
        self._client.delete_grant(self.role_id, self.id)
