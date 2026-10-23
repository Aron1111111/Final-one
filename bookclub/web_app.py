"""Local BookClub web demo using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import threading
from copy import deepcopy
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .errors import DomainError
from .status_transitions import ALLOWED, transition_status


WEB_ROOT = Path(__file__).resolve().parent.parent / "web"

INITIAL_MEETINGS = [
    {
        "id": 1,
        "title": "Мастер и Маргарита",
        "startsAt": "2026-11-01T15:00:00+03:00",
        "location": "Городская библиотека, зал 2",
        "description": "Читаем ключевые главы и обсуждаем выбор героев и отражение реальности в романе.",
        "status": "published",
    },
    {
        "id": 2,
        "title": "Паттерны проектирования в Python",
        "startsAt": "2026-11-08T14:00:00+08:00",
        "location": "Онлайн-зал",
        "description": "Разбираем распространённые паттерны на коротких примерах и обсуждаем практические компромиссы.",
        "status": "draft",
    },
    {
        "id": 3,
        "title": "Маленький принц: новое прочтение",
        "startsAt": "2026-10-18T10:00:00+08:00",
        "location": "Клубный читальный зал",
        "description": "Перечитываем повесть глазами взрослых и делимся отрывками, которые тронули сильнее всего.",
        "status": "completed",
    },
]

USERS = {
    "member-demo": {"id": 17, "role": "member"},
    "organizer-demo": {"id": 1, "role": "organizer"},
}


class BookClubState:
    """Thread-safe in-memory state for the local demo."""

    lock = threading.RLock()
    meetings = deepcopy(INITIAL_MEETINGS)
    registrations: dict[tuple[int, int], dict] = {}
    next_registration_id = 1

    @classmethod
    def reset(cls) -> None:
        with cls.lock:
            cls.meetings = deepcopy(INITIAL_MEETINGS)
            cls.registrations = {}
            cls.next_registration_id = 1


class BookClubHandler(BaseHTTPRequestHandler):
    server_version = "BookClubLocal/1.0"

    def log_message(self, message: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {message % args}")

    def _send_bytes(
        self,
        status: int,
        payload: bytes,
        content_type: str,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _send_json(self, status: int, payload: object) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send_bytes(status, data, "application/json; charset=utf-8")

    def _send_error_json(self, status: int, code: str, message: str) -> None:
        self._send_json(status, {"code": code, "message": message})

    def _serve_asset(self, name: str, content_type: str) -> None:
        path = WEB_ROOT / name
        if not path.is_file():
            self._send_error_json(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Ресурс не найден")
            return
        self._send_bytes(HTTPStatus.OK, path.read_bytes(), content_type)

    def _current_user(self) -> dict | None:
        value = self.headers.get("Authorization", "")
        if not value.startswith("Bearer "):
            return None
        return USERS.get(value.removeprefix("Bearer ").strip())

    def _meeting(self, meeting_id: int) -> dict | None:
        return next(
            (meeting for meeting in BookClubState.meetings if meeting["id"] == meeting_id),
            None,
        )

    def _read_json(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            value = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_asset("index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/styles.css":
            self._serve_asset("styles.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/app.js":
            self._serve_asset("app.js", "text/javascript; charset=utf-8")
            return
        if parsed.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "service": "bookclub"})
            return
        if parsed.path == "/meetings":
            self._list_meetings(parsed.query)
            return
        self._send_error_json(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Ресурс не найден")

    def _list_meetings(self, query: str) -> None:
        values = parse_qs(query)
        try:
            limit = int(values.get("limit", ["20"])[0])
            offset = int(values.get("offset", ["0"])[0])
        except ValueError:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "INVALID_PAGINATION", "limit и offset должны быть целыми числами")
            return
        if not 1 <= limit <= 100 or offset < 0:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "INVALID_PAGINATION", "limit должен быть от 1 до 100, offset — не меньше 0")
            return
        with BookClubState.lock:
            result = deepcopy(BookClubState.meetings[offset : offset + limit])
        self._send_json(HTTPStatus.OK, result)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        match = re.fullmatch(r"/meetings/(\d+)/registrations", parsed.path)
        if match:
            self._register(int(match.group(1)))
            return
        self._send_error_json(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Ресурс не найден")

    def _register(self, meeting_id: int) -> None:
        user = self._current_user()
        if user is None:
            self._send_error_json(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Требуется действительный Bearer-токен")
            return
        with BookClubState.lock:
            meeting = self._meeting(meeting_id)
            if meeting is None:
                self._send_error_json(HTTPStatus.NOT_FOUND, "MEETING_NOT_FOUND", "Встреча не найдена")
                return
            key = (meeting_id, user["id"])
            if key in BookClubState.registrations:
                self._send_error_json(HTTPStatus.CONFLICT, "ALREADY_REGISTERED", "Вы уже записаны на эту встречу")
                return
            registration = {
                "id": BookClubState.next_registration_id,
                "meetingId": meeting_id,
                "memberId": user["id"],
                "createdAt": datetime.now(timezone.utc).isoformat(),
            }
            BookClubState.next_registration_id += 1
            BookClubState.registrations[key] = registration
        self._send_json(HTTPStatus.CREATED, registration)

    def do_PATCH(self) -> None:
        parsed = urlparse(self.path)
        match = re.fullmatch(r"/meetings/(\d+)/status", parsed.path)
        if match:
            self._change_status(int(match.group(1)))
            return
        self._send_error_json(HTTPStatus.NOT_FOUND, "NOT_FOUND", "Ресурс не найден")

    def _change_status(self, meeting_id: int) -> None:
        user = self._current_user()
        if user is None:
            self._send_error_json(HTTPStatus.UNAUTHORIZED, "UNAUTHORIZED", "Требуется действительный Bearer-токен")
            return
        body = self._read_json()
        if body is None or "status" not in body:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "INVALID_STATUS", "Необходимо указать статус")
            return
        with BookClubState.lock:
            meeting = self._meeting(meeting_id)
            if meeting is None:
                self._send_error_json(HTTPStatus.NOT_FOUND, "MEETING_NOT_FOUND", "Встреча не найдена")
                return
            try:
                target = transition_status(meeting["status"], body["status"], user["role"])
            except DomainError as error:
                status = {
                    "ROLE_FORBIDDEN": HTTPStatus.FORBIDDEN,
                    "INVALID_STATUS": HTTPStatus.BAD_REQUEST,
                    "INVALID_STATUS_TRANSITION": HTTPStatus.CONFLICT,
                }[error.code]
                self._send_error_json(status, error.code, str(error))
                return
            meeting["status"] = target
            result = deepcopy(meeting)
        self._send_json(HTTPStatus.OK, result)


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), BookClubHandler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local BookClub web demo")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = create_server(args.host, args.port)
    print(f"BookClub is available at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping BookClub")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
