#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
HOST="${FALTANTE_HOST:-127.0.0.1}"
PORT="${FALTANTE_PORT:-8090}"
LOG_LEVEL="${FALTANTE_LOG_LEVEL:-INFO}"
SERVICE_NAME="${FALTANTE_SERVICE_NAME:-faltante}"
HEALTH_STATUS="${FALTANTE_HEALTH_STATUS:-ok}"

exec "${PYTHON_BIN}" "${SCRIPT_DIR}/faltante_service.py" \
  --host "${HOST}" \
  --port "${PORT}" \
  --log-level "${LOG_LEVEL}" \
  --service-name "${SERVICE_NAME}" \
  --health-status "${HEALTH_STATUS}" \
  "$@"
