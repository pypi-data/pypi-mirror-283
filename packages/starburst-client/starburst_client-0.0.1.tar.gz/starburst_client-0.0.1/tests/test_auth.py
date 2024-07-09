import unittest

from starburst_client.auth import BasicAuth, JWT


class TestAuth(unittest.TestCase):
    def test_basic_auth(self):
        basic_auth = BasicAuth("Aladdin", "open sesame")

        self.assertEqual(basic_auth.token, "QWxhZGRpbjpvcGVuIHNlc2FtZQ==")

    def test_jwt(self):
        jwt = JWT("TokenText")

        self.assertEqual(jwt.token, "TokenText")
