#!/usr/bin/env bash
set -euo pipefail

if ! command -v systemctl >/dev/null 2>&1; then
  echo "systemctl no está disponible en este host. Ejecuta este script en un servidor con systemd." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
UNIT_TEMPLATE="${REPO_ROOT}/systemd/faltante.service"

EXEC_START="${FALTANTE_EXEC_START:-${REPO_ROOT}/scripts/run_faltante.sh}"
WORKING_DIR="${FALTANTE_WORKING_DIR:-${REPO_ROOT}}"
ENV_FILE="${FALTANTE_ENV_FILE:-/etc/faltante.env}"
RUN_USER="${FALTANTE_USER:-root}"
RUN_GROUP="${FALTANTE_GROUP:-${RUN_USER}}"
UNIT_TARGET="${FALTANTE_UNIT_PATH:-/etc/systemd/system/faltante.service}"
ENABLE_UNIT="${FALTANTE_ENABLE:-1}"

if [[ ! -x "${EXEC_START}" ]]; then
  echo "Advertencia: ${EXEC_START} no es ejecutable. Ajusta FALTANTE_EXEC_START antes de instalar." >&2
fi

TMP_UNIT="$(mktemp)"
trap 'rm -f "${TMP_UNIT}"' EXIT

sed \
  -e "s|{{EXEC_START}}|${EXEC_START}|g" \
  -e "s|{{WORKING_DIR}}|${WORKING_DIR}|g" \
  -e "s|{{ENV_FILE}}|${ENV_FILE}|g" \
  -e "s|{{USER}}|${RUN_USER}|g" \
  -e "s|{{GROUP}}|${RUN_GROUP}|g" \
  "${UNIT_TEMPLATE}" > "${TMP_UNIT}"

sudo install -Dm0644 "${TMP_UNIT}" "${UNIT_TARGET}"

sudo systemctl daemon-reload
if [[ "${ENABLE_UNIT}" == "1" ]]; then
  sudo systemctl enable faltante.service
fi

echo "Unidad instalada en ${UNIT_TARGET}. Ejecuta 'sudo systemctl restart faltante.service' para iniciar el servicio."
