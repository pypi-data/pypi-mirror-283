from enum import Enum

import requests


class ErrorCode(Enum):
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    SQL_SYNTAX_ERROR = "SQL_SYNTAX_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    NOT_FOUND = "NOT_FOUND"
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class Error(Exception):
    """base error class"""

    pass


class UnauthorizedError(Error):
    """Status: 401 - Unauthorized"""

    pass


class ApiError(Error):
    """API Errors"""

    def __init__(self, error: dict):
        self._error = error

    @property
    def error_code(self) -> ErrorCode | None:
        return ErrorCode(self._error.get("errorCode", None))

    @property
    def message(self) -> str | None:
        return self._error.get("message", None)

    @property
    def details_type(self) -> str | None:
        return self._error.get("detailsType", None)

    @property
    def details(self) -> dict | None:
        return self._error.get("details", None)

    def __repr__(self) -> str:
        return '{}(error_code={}, message="{}", details_type={}, details="{}")'.format(
            self.__class__.__name__,
            self.error_code,
            self.message,
            self.details_type,
            self.details,
        )

    def __str__(self) -> str:
        return repr(self)


class BadRequestError(ApiError):
    """Status: 400 - Bad Request"""

    pass


class ForbiddenError(ApiError):
    """Status: 403 - Forbidden"""

    pass


class NotFoundError(ApiError):
    """Status: 404 - Not found"""

    pass


class ConflictError(ApiError):
    """Status: 409 - Conflict"""

    pass


def raise_for_api_errors(resp: requests.Response, **kwargs):
    if resp.ok:
        return

    if resp.status_code == 401:
        raise UnauthorizedError()

    try:
        error_data = resp.json()
    except requests.exceptions.JSONDecodeError:
        content = resp.content.decode("utf-8")
        raise Error(
            f"Unexpected error that cannot be decoded from JSON, status={resp.status_code} content={content}"
        )

    if resp.status_code == 400:
        raise BadRequestError(error_data)
    elif resp.status_code == 403:
        raise ForbiddenError(error_data)
    elif resp.status_code == 404:
        raise NotFoundError(error_data)
    elif resp.status_code == 409:
        raise ConflictError(error_data)
    else:
        raise ApiError(error_data)
