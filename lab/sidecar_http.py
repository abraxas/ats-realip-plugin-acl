#!/usr/bin/env python3
"""HTTP probe run inside compose sidecars (attacker / trusted)."""

from __future__ import annotations

import argparse
import json
import socket
import urllib.error
import urllib.request


def request_url(
    url: str,
    method: str,
    host: str | None,
    extra_headers: list[str],
    timeout: float,
) -> tuple[int, str, str]:
    headers: dict[str, str] = {}
    if host:
        headers["Host"] = host
    for item in extra_headers:
        name, sep, value = item.partition(":")
        if not sep:
            continue
        headers[name.strip()] = value.strip()
    req = urllib.request.Request(url, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace")
            peer = ""
            sock = getattr(resp, "fp", None)
            raw = getattr(sock, "raw", None)
            inner = getattr(raw, "_sock", None)
            if inner is not None:
                try:
                    peer = str(inner.getpeername())
                except OSError:
                    peer = ""
            return int(resp.status), body, peer
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return int(exc.code), body, ""
    except urllib.error.URLError as exc:
        return 0, str(exc.reason), ""
    except TimeoutError:
        return 0, "timeout", ""
    except socket.timeout:
        return 0, "timeout", ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Sidecar HTTP probe")
    parser.add_argument("--url", required=True)
    parser.add_argument("--method", default="GET")
    parser.add_argument("--host")
    parser.add_argument("--header", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=8.0)
    args = parser.parse_args()
    status, body, peer = request_url(
        args.url,
        args.method,
        args.host,
        args.header,
        args.timeout,
    )
    print(
        json.dumps(
            {
                "status": status,
                "body": body,
                "peer": peer,
            }
        ),
        flush=True,
    )
    return 0 if status else 1


if __name__ == "__main__":
    raise SystemExit(main())
