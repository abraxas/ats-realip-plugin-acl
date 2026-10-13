#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-ats-realip-plugin-acl}"
export PYTHONUNBUFFERED=1
export ATS_URL="${ATS_URL:-http://127.0.0.1:18770}"
export ORIGIN_URL="${ORIGIN_URL:-http://127.0.0.1:18771}"

LABEL="ats-realip-plugin-acl"
WITNESS="ATS-REALIP-PLUGIN-ACL-WITNESS"
IMAGE="ats-10.2.0-lab:local"
SRC_REL="../../client-reviews/trafficserver/src"
SRC_COPY="/tmp/ats-10.2.0-src"
LOCK="/tmp/ats-10.2.0-lab.lock"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

trap down EXIT

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 || true
  exit 1
}

ensure_ats_image() {
  echo "== lock ${LOCK} for ${IMAGE} =="
  LOCK="${LOCK}" IMAGE="${IMAGE}" SRC_REL="${SRC_REL}" SRC_COPY="${SRC_COPY}" python3 - <<'PY'
import fcntl
import os
import subprocess
import sys

lock_path = os.environ["LOCK"]
image = os.environ["IMAGE"]
src_rel = os.environ["SRC_REL"]
src_copy = os.environ["SRC_COPY"]
fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
fcntl.flock(fd, fcntl.LOCK_EX)


def has_realip() -> bool:
    inspect = subprocess.run(
        ["docker", "image", "inspect", image],
        capture_output=True,
        check=False,
    )
    if inspect.returncode != 0:
        return False
    check = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/bin/sh",
            image,
            "-c",
            "test -f /opt/ats/libexec/trafficserver/realip.so",
        ],
        check=False,
    )
    return check.returncode == 0


if has_realip():
    print(f"IOC shared-image-present {image} realip.so", flush=True)
    sys.exit(0)

print(f"== rsync ATS 10.2.0 source and build {image} ==", flush=True)
os.makedirs(src_copy, exist_ok=True)
subprocess.check_call(
    [
        "rsync",
        "-a",
        "--delete",
        "--exclude",
        ".git",
        "--exclude",
        "doc",
        "--exclude",
        "tests",
        "--exclude",
        "ci",
        src_rel.rstrip("/") + "/",
        src_copy.rstrip("/") + "/",
    ]
)
subprocess.check_call(["cp", "-f", "Dockerfile.base", os.path.join(src_copy, "Dockerfile.base")])
subprocess.check_call(["docker", "build", "-t", image, "-f", "Dockerfile.base", src_copy])
sys.exit(0 if has_realip() else 2)
PY
  local rc=$?
  if [[ "${rc}" != 0 ]]; then
    fail_setup "ats-image-build-failed rc=${rc}"
  fi
}

echo "== docker compose down (clean) =="
down

if ! docker image inspect python:3.13-slim >/dev/null 2>&1; then
  echo "== docker pull python:3.13-slim =="
  docker pull python:3.13-slim || fail_setup "python-image-pull-failed"
fi

ensure_ats_image

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 20); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up -d --build; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 20
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
