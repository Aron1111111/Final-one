import http.client
import json
import threading
import unittest

from bookclub.web_app import BookClubState, create_server


class WebAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def setUp(self):
        BookClubState.reset()

    def request(self, method, path, body=None, token=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if body is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(body)
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        connection.close()
        return response.status, payload

    def test_lists_meetings(self):
        status, payload = self.request("GET", "/meetings")
        self.assertEqual(status, 200)
        self.assertEqual(len(payload), 3)

    def test_rejects_invalid_pagination(self):
        status, payload = self.request("GET", "/meetings?limit=0")
        self.assertEqual(status, 400)
        self.assertEqual(payload["code"], "INVALID_PAGINATION")

    def test_registration_requires_authentication(self):
        status, payload = self.request("POST", "/meetings/1/registrations")
        self.assertEqual(status, 401)
        self.assertEqual(payload["code"], "UNAUTHORIZED")

    def test_registration_and_duplicate(self):
        status, payload = self.request(
            "POST", "/meetings/1/registrations", token="member-demo"
        )
        self.assertEqual(status, 201)
        self.assertEqual(payload["meetingId"], 1)
        status, payload = self.request(
            "POST", "/meetings/1/registrations", token="member-demo"
        )
        self.assertEqual(status, 409)
        self.assertEqual(payload["code"], "ALREADY_REGISTERED")

    def test_member_cannot_change_status(self):
        status, payload = self.request(
            "PATCH",
            "/meetings/2/status",
            {"status": "published"},
            token="member-demo",
        )
        self.assertEqual(status, 403)
        self.assertEqual(payload["code"], "ROLE_FORBIDDEN")

    def test_organizer_changes_status(self):
        status, payload = self.request(
            "PATCH",
            "/meetings/2/status",
            {"status": "published"},
            token="organizer-demo",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "published")


if __name__ == "__main__":
    unittest.main()
