#!/usr/bin/env python3
"""Origin for the realip PLUGIN remap ACL leftover lab."""

from __future__ import annotations

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

WITNESS = os.environ.get("WITNESS", "ATS-REALIP-PLUGIN-ACL-WITNESS")
LISTEN_HOST = os.environ.get("ORIGIN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("ORIGIN_PORT", "8080"))


class OriginHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"origin {self.address_string()} {fmt % args}", flush=True)

    def _send(self, status: int, body: str) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path.startswith("/secret"):
            self._send(200, f"{WITNESS}\n")
            return
        if path.startswith("/denied"):
            self._send(200, "DENIED\n")
            return
        self._send(200, "OTHER\n")

    def do_PURGE(self) -> None:
        self._send(200, "ORIGIN-PURGE\n")


def main() -> int:
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), OriginHandler)
    print(f"origin-listen {LISTEN_HOST}:{LISTEN_PORT}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
