import abc
import base64


class Auth(abc.ABC):
    """
    This class is the base class of all authentication methods for Requester.
    """

    @property
    @abc.abstractmethod
    def token_type(self) -> str:
        """
        The type of the auth token as used in the HTTP Authorization header, e.g. Bearer or Basic.

        :return: token type

        """

    @property
    @abc.abstractmethod
    def token(self) -> str:
        """
        The auth token as used in the HTTP Authorization header.

        :return: token

        """


class BasicAuth(Auth):
    def __init__(self, login: str, password: str):
        assert isinstance(login, str)
        assert len(login) > 0
        assert isinstance(password, str)
        assert len(password) > 0

        self._login = login
        self._password = password

    @property
    def login(self) -> str:
        return self._login

    @property
    def username(self) -> str:
        return self.login

    @property
    def password(self) -> str:
        return self._password

    @property
    def token(self) -> str:
        credentials = f"{self.login}:{self.password}"
        credentials_base64 = base64.b64encode(bytes(credentials, "UTF-8")).decode()
        return credentials_base64

    @property
    def token_type(self) -> str:
        return "Basic"


class JWT(Auth):
    def __init__(self, token: str):
        assert isinstance(token, str)
        assert len(token) > 0
        self._token = token

    @property
    def token(self) -> str:
        return self._token

    @property
    def token_type(self) -> str:
        return "Bearer"
