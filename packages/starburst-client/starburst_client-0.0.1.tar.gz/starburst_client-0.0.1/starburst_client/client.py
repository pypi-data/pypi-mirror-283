from enum import Enum
from datetime import date, datetime

import requests

from starburst_client.auth import Auth
from starburst_client.exceptions import raise_for_api_errors
from starburst_client._version import __version__

_ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Action(Enum):
    SHOW = "SHOW"
    CREATE = "CREATE"
    ALTER = "ALTER"
    DROP = "DROP"
    EXECUTE = "EXECUTE"
    SELECT = "SELECT"
    INSERT = "INSERT"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    REFRESH = "REFRESH"
    IMPERSONATE = "IMPERSONATE"
    KILL = "KILL"
    SET = "SET"
    PUBLISH = "PUBLISH"
    READ = "READ"
    WRITE = "WRITE"


class Category(Enum):
    TABLES = "TABLES"
    SCHEMA_PROPERTIES = "SCHEMA_PROPERTIES"
    TABLE_PROPERTIES = "TABLE_PROPERTIES"
    SYSTEM_SESSION_PROPERTIES = "SYSTEM_SESSION_PROPERTIES"
    CATALOG_SESSION_PROPERTIES = "CATALOG_SESSION_PROPERTIES"
    FUNCTIONS = "FUNCTIONS"
    PROCEDURES = "PROCEDURES"
    QUERIES = "QUERIES"
    ROLES = "ROLES"
    USERS = "USERS"
    DATA_PRODUCTS = "DATA_PRODUCTS"
    AUDIT_LOGS = "AUDIT_LOGS"
    SYSTEM_INFORMATION = "SYSTEM_INFORMATION"


class Effect(Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_GRANT_OPTION = "ALLOW_WITH_GRANT_OPTION"
    DENY = "DENY"


class Client:
    def __init__(self, base_url: str, auth: None | Auth = None) -> None:
        self.__base_url = base_url
        self.session = requests.Session()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"Starburst Python Client/{__version__}",
        }
        if auth:
            headers["Authorization"] = f"{auth.token_type} {auth.token}"
        self.session.headers.update(headers)
        self.session.hooks["response"].append(raise_for_api_errors)

    def _paginate(
        self,
        url: str,
        page_size: int = 100,
        page_sort: str = "ASC",
        filter: None | dict = None,
    ):
        params: dict[str, str | int] = {
            "pageToken": "",
            "pageSize": page_size,
            "pageSort": page_sort,
        }
        if filter:
            params.update(filter)
        while True:
            data = self.session.get(url, params=params).json()
            for item in data["result"]:
                yield item

            if "nextPageToken" in data:
                params["pageToken"] = data["nextPageToken"]
            else:
                break

    # AuditLogs
    def list_access_logs(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        query_id: str | None = None,
    ):
        """List Starburst built-in access control access logs"""
        assert start_date is None or isinstance(
            start_date, (datetime, date)
        ), start_date
        assert end_date is None or isinstance(end_date, (datetime, date)), end_date
        assert query_id is None or isinstance(query_id, int), query_id

        filter = {}
        if start_date:
            filter["startDate"] = start_date.strftime(_ISO_DATE_FORMAT)
        if end_date:
            filter["endDate"] = end_date.strftime(_ISO_DATE_FORMAT)
        if query_id:
            filter["queryId"] = query_id

        return self._paginate(f"{self.__base_url}/biac/audit/accessLogs", filter=filter)

    def list_change_logs(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        query_id: str | None = None,
    ):
        """List Starburst built-in access control change logs"""
        assert start_date is None or isinstance(
            start_date, (datetime, date)
        ), start_date
        assert end_date is None or isinstance(end_date, (datetime, date)), end_date
        assert query_id is None or isinstance(query_id, int), query_id

        filter = {}
        if start_date:
            filter["startDate"] = start_date.strftime(_ISO_DATE_FORMAT)
        if end_date:
            filter["endDate"] = end_date.strftime(_ISO_DATE_FORMAT)
        if query_id:
            filter["queryId"] = query_id
        return self._paginate(f"{self.__base_url}/biac/audit/changeLogs", filter=filter)

    # ColumnMasks
    def add_column_mask_to_role(self, role_id: int):
        """Add a column mask to a role to mask column values from subjects assigned to the role."""
        assert isinstance(role_id, int), role_id
        # /api/v1/biac/roles/{roleId}/columnMasks
        raise NotImplementedError

    def create_column_mask_expression(self):
        """Create an expression that can be applied to mask column values"""
        # /api/v1/biac/expressions/columnMask
        raise NotImplementedError

    def delete_column_mask_expression(self, column_mask_expression_id: int):
        """Delete a column mask expression"""
        assert isinstance(column_mask_expression_id, int), column_mask_expression_id

        self.session.delete(
            f"{self.__base_url}/biac/expressions/columnMask/{column_mask_expression_id}"
        )

    def delete_role_column_mask(self, role_id: int, column_mask_id: int):
        """Remove a column mask from a role."""
        assert isinstance(role_id, int), role_id
        assert isinstance(column_mask_id, int), column_mask_id

        self.session.delete(
            f"{self.__base_url}/biac/roles/{role_id}/columnMasks/{column_mask_id}"
        )

    def get_column_mask(self, role_id: int, column_mask_id: int):
        """Get a column mask of a given role."""
        assert isinstance(role_id, int), role_id
        assert isinstance(column_mask_id, int), column_mask_id

        return self.session.get(
            f"{self.__base_url}/biac/roles/{role_id}/columnMasks/{column_mask_id}"
        ).json()

    def get_column_mask_expression(self, column_mask_expression_id: int):
        """Get an expression that can be used to mask column values"""
        assert isinstance(column_mask_expression_id, int), column_mask_expression_id

        return self.session.get(
            f"{self.__base_url}/biac/expressions/columnMask//{column_mask_expression_id}"
        ).json()

    def list_column_mask_expressions(self):
        """List the expressions that can be used to mask column values"""

        return self._paginate(f"{self.__base_url}/biac/expressions/columnMask")

    def list_role_column_masks(self, role_id: int):
        """List all the column masks of a role."""
        assert isinstance(role_id, int), role_id

        return self._paginate(f"{self.__base_url}/biac/roles/{role_id}/columnMasks")

    def update_column_mask_expression(self):
        """Update a column mask expression"""
        # PUT /api/v1/biac/expressions/columnMask/{columnMaskExpressionId}
        raise NotImplementedError

    # EntityCategories
    def list_available_actions(self, entity_category: str):
        """List all actions that can be allowed or denied for an EntityCategory"""
        assert isinstance(entity_category, str), entity_category

        return self._paginate(
            f"{self.__base_url}/biac/entityCategories/{entity_category}/actions"
        )

    def list_entity_categories(self):
        return self._paginate(f"{self.__base_url}/biac/entityCategories")

    # Grants
    def create_grant(self, role_id: int, effect: Effect, action: Action, entity: dict):
        """Create a Starburst built-in access control grant for a role"""
        # assert isinstance(role_id, int), role_id
        assert effect in Effect, effect
        assert action in Action, action
        assert "category" in entity, entity
        assert entity["category"] in Category, entity["category"]

        return self.session.post(
            f"{self.__base_url}/biac/roles/{role_id}/grants",
            json={"effect": effect, "action": action, "entity": entity},
        ).json()

    def delete_grant(self, role_id: int, grant_id: int):
        """Delete a Starburst built-in access control grant of a role"""
        assert isinstance(role_id, int), role_id
        assert isinstance(grant_id, int), grant_id

        self.session.delete(f"{self.__base_url}/biac/roles/{role_id}/grants/{grant_id}")

    def get_grant(self, role_id: int, grant_id: int):
        """Get a Starburst built-in access control grant of a role"""
        assert isinstance(role_id, int), role_id
        assert isinstance(grant_id, int), grant_id

        return self.session.get(
            f"{self.__base_url}/biac/roles/{role_id}/grants/{grant_id}"
        ).json()

    def list_grants(self, role_id: int):
        """List Starburst built-in access control grants of a role"""
        assert isinstance(role_id, int), role_id

        return self._paginate(f"{self.__base_url}/biac/roles/{role_id}/grants")

    # LocationGrants
    def add_location_grant(self, role_id: int):
        """Add a LocationGrant to a role to allow accessing that location by the given role."""
        assert isinstance(role_id, int), role_id

        # /api/v1/biac/roles/{roleId}/locationGrants
        raise NotImplementedError

    def deleteLocationGrant(self, role_id: int, location_grant_id: int):
        """Remove a LocationGrant from a role."""
        assert isinstance(role_id, int), role_id
        assert isinstance(location_grant_id, int), location_grant_id

        self.session.delete(
            f"{self.__base_url}/biac/roles/{role_id}/locationGrants/{location_grant_id}"
        )

    def get_location_grant(self, role_id: int, location_grant_id: int):
        """Get a Starburst built-in access control location grant of a role"""
        assert isinstance(role_id, int), role_id
        assert isinstance(location_grant_id, int), location_grant_id

        return self.session.get(
            f"{self.__base_url}/biac/roles/{role_id}/locationGrants/{location_grant_id}"
        ).json()

    def list_location_grants(self, role_id: int):
        """List Starburst built-in access control location grants of a role"""
        assert isinstance(role_id, int), role_id

        return self._paginate(f"{self.__base_url}/biac/roles/{role_id}/locationGrants")

    # RoleAssignments
    def list_role_assignments(self, role_id: int):
        """List assignments of a Starburst built-in access control role"""
        assert isinstance(role_id, int), role_id

        return self._paginate(f"{self.__base_url}/biac/roles/{role_id}/assignments")

    # RowFilters
    def add_row_filter_to_role(self, role_id: int):
        """Add a row filter to a role to filter out table rows from queries made by subjects assigned to the role."""
        assert isinstance(role_id, int), role_id

        # /api/v1/biac/roles/{roleId}/rowFilters
        raise NotImplementedError

    def create_row_filter_expression(self):
        """Create an expression that can be applied to filter table rows from query results"""

        # /api/v1/biac/expressions/rowFilter
        raise NotImplementedError

    def delete_role_row_filter(self, role_id: int, row_filter_id: int):
        """Remove a row filter from a role."""
        assert isinstance(role_id, int), role_id
        assert isinstance(row_filter_id, int), row_filter_id

        self.session.delete(
            f"{self.__base_url}/biac/roles/{role_id}/rowFilters/{row_filter_id}"
        )

    def delete_row_filter_expression(self, row_filter_expression_id: int):
        """Delete a row filter expression"""
        assert isinstance(row_filter_expression_id, int), row_filter_expression_id

        self.session.delete(
            f"{self.__base_url}/biac/expressions/rowFilter/{row_filter_expression_id}"
        )

    def get_row_filter(self, role_id: int, row_filter_id: int):
        """Get a row filter of a given role."""
        assert isinstance(role_id, int), role_id
        assert isinstance(row_filter_id, int), row_filter_id

        return self.session.get(
            f"{self.__base_url}/biac/roles/{role_id}/rowFilters/{row_filter_id}"
        ).json()

    def get_row_filter_expression(self, row_filter_expression_id: int):
        """Get an expression that can be applied to filter table rows from query results"""
        assert isinstance(row_filter_expression_id, int), row_filter_expression_id

        return self.session.get(
            f"{self.__base_url}/biac/expressions/rowFilter/{row_filter_expression_id}"
        ).json()

    def list_role_row_filters(self, role_id: int):
        """List all the rows filters of a role."""
        assert isinstance(role_id, int), role_id

        return self.session.get(
            f"{self.__base_url}/biac/roles/{role_id}/rowFilters"
        ).json()

    def list_row_filter_expressions(self):
        """List expressions that can be applied to filter table rows from query results"""

        return self._paginate(f"{self.__base_url}/biac/expressions/rowFilter")

    def update_row_filter_expression(self):
        """Update a row filter expression"""

        # /api/v1/biac/expressions/rowFilter/{rowFilterExpressionId}
        raise NotImplementedError

    # Roles
    def create_role(self, name: str, description: str | None = None) -> dict:
        """Create a Starburst built-in access control role and returns the role ID"""
        assert isinstance(name, str), name
        assert description is None or isinstance(description, str), description

        return self.session.post(
            f"{self.__base_url}/biac/roles",
            json={"name": name, "description": description},
        ).json()

    def delete_role(self, role_id: int) -> None:
        """Delete a Starburst built-in access control role"""
        assert isinstance(role_id, int), role_id

        self.session.delete(f"{self.__base_url}/biac/roles/{role_id}")

    def get_role(self, role_id: int) -> dict:
        """Get a Starburst built-in access control role"""
        assert isinstance(role_id, int), role_id

        return self.session.get(f"{self.__base_url}/biac/roles/{role_id}").json()

    def list_roles(self):
        """List Starburst built-in access control roles"""

        return self._paginate(f"{self.__base_url}/biac/roles/")

    def update_role(self, role_id: int, name: str, description: str | None = None):
        """Update a Starburst built-in access control role"""
        assert isinstance(role_id, int), role_id
        assert isinstance(name, str), name
        assert description is None or isinstance(description, str), description

        return self.session.put(
            f"{self.__base_url}/biac/roles/{role_id}",
            json={"name": name, "description": description},
        ).json()

    # Subjects
    def create_role_assignment_for_group(
        self, group_name: str, role_id: int, role_admin: bool = False
    ):
        """Assign a Starburst built-in access control role to the given group"""
        assert isinstance(group_name, str), group_name
        assert isinstance(role_id, int), role_id
        assert isinstance(role_admin, bool), role_admin

        return self.session.post(
            f"{self.__base_url}/biac/subjects/groups/{group_name}/assignments",
            json={"roleId": role_id, "roleAdmin": role_admin},
        ).json()

    def create_role_assignment_for_role(
        self, subject_role_id: int, role_id: int, role_admin: bool = False
    ):
        """Assign a Starburst built-in access control role to the given role"""
        assert isinstance(subject_role_id, int), subject_role_id
        assert isinstance(role_id, int), role_id
        assert isinstance(role_admin, bool), role_admin

        return self.session.post(
            f"{self.__base_url}/biac/subjects/roles/{subject_role_id}/assignments",
            json={"roleId": role_id, "roleAdmin": role_admin},
        ).json()

    def create_role_assignment_for_user(
        self, username: str, role_id: int, role_admin: bool = False
    ) -> dict:
        """Assign a Starburst built-in access control role to the given user"""
        assert isinstance(username, str), username
        assert isinstance(role_id, int), role_id
        assert isinstance(role_admin, bool), role_admin

        return self.session.post(
            f"{self.__base_url}/biac/subjects/users/{username}/assignments",
            json={"roleId": role_id, "roleAdmin": role_admin},
        ).json()

    def delete_role_assignment_from_group(self, group_name: str, assignment_id: int):
        """Delete an assignment to a Starburst built-in access control role from the given group"""
        assert isinstance(group_name, str), group_name
        assert isinstance(assignment_id, int), assignment_id

        self.session.delete(
            f"{self.__base_url}/biac/subjects/groups/{group_name}/assignments/{assignment_id}"
        )

    def delete_role_assignment_from_role(
        self, subject_role_id: int, assignment_id: int
    ):
        """Delete an assignment to a Starburst built-in access control role from the given role"""
        assert isinstance(subject_role_id, int), subject_role_id
        assert isinstance(assignment_id, int), assignment_id

        self.session.delete(
            f"{self.__base_url}/biac/subjects/roles/{subject_role_id}/assignments/{assignment_id}"
        )

    def delete_role_assignment_from_user(self, username: str, assignment_id: int):
        """Delete an assignment to a Starburst built-in access control role from the given user"""
        assert isinstance(username, str), username
        assert isinstance(assignment_id, int), assignment_id

        self.session.delete(
            f"{self.__base_url}/biac/subjects/users/{username}/assignments/{assignment_id}"
        )

    def get_role_assignments_for_group(self, group_name: str):
        """Get all Starburst built-in access control roles assigned to the given group"""
        assert isinstance(group_name, str), group_name

        return self._paginate(
            f"{self.__base_url}/biac/subjects/groups/{group_name}/assignments"
        )

    def get_role_assignments_for_role(self, role_id: int):
        """Get all Starburst built-in access control roles assigned to the given role"""
        assert isinstance(role_id, int), role_id

        return self._paginate(
            f"{self.__base_url}/biac/subjects/roles/{role_id}/assignments"
        )

    def get_role_assignments_for_user(self, username: str):
        """Get all Starburst built-in access control roles assigned to the given user"""
        assert isinstance(username, str), username

        return self._paginate(
            f"{self.__base_url}/biac/subjects/users/{username}/assignments"
        )
