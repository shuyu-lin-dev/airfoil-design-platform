import asyncio
import json
from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass
class ASGIResponse:
    status_code: int
    body: bytes

    def json(self):
        return json.loads(self.body.decode("utf-8"))

    @property
    def text(self):
        return self.body.decode("utf-8")


class SyncASGIClient:
    def __init__(self, app):
        self.app = app

    def get(self, path):
        return self.request("GET", path)

    def post(self, path, json=None):
        headers = [(b"content-type", b"application/json")]
        body = b"" if json is None else _json_bytes(json)
        return self.request("POST", path, body=body, headers=headers)

    def request(self, method, path, body=b"", headers=None):
        return asyncio.run(self._request(method, path, body, headers or []))

    async def _request(self, method, path, body, headers):
        parts = urlsplit(path)
        messages = []
        request_sent = False

        async def receive():
            nonlocal request_sent
            if request_sent:
                return {"type": "http.disconnect"}
            request_sent = True
            return {"type": "http.request", "body": body, "more_body": False}

        async def send(message):
            messages.append(message)

        await self.app(_scope(method, parts, headers), receive, send)
        return _response_from(messages)


def _json_bytes(value):
    return json.dumps(value).encode("utf-8")


def _scope(method, parts, headers):
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": parts.path,
        "raw_path": parts.path.encode("ascii"),
        "query_string": parts.query.encode("ascii"),
        "root_path": "",
        "headers": [(b"host", b"testserver")] + headers,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }


def _response_from(messages):
    status_code = 500
    body_parts = []
    for message in messages:
        if message["type"] == "http.response.start":
            status_code = message["status"]
        elif message["type"] == "http.response.body":
            body_parts.append(message.get("body", b""))
    return ASGIResponse(status_code=status_code, body=b"".join(body_parts))
