#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VALIDATE_SCRIPT="${SCRIPT_DIR}/validate_faltante.sh"

if [[ ! -x "${VALIDATE_SCRIPT}" ]]; then
  echo "No se encontró ${VALIDATE_SCRIPT}. Asegúrate de ejecutar este script desde el repositorio original." >&2
  exit 1
fi

HOST="${FALTANTE_VALIDATE_HOST:-127.0.0.1}"
PORT="${FALTANTE_VALIDATE_PORT:-8090}"
SERVICE_NAME="${FALTANTE_SERVICE_NAME:-faltante}"
TIMEOUT="${FALTANTE_VALIDATE_TIMEOUT:-5}"
KILL_ON_CONFLICT="${FALTANTE_KILL_PORT:-0}"
JOURNAL_LINES="${FALTANTE_JOURNAL_LINES:-100}"
OUTPUT_DIR="${FALTANTE_EVIDENCE_DIR:-${REPO_ROOT}/artifacts}"
mkdir -p "${OUTPUT_DIR}"

TIMESTAMP="$(date '+%Y%m%d-%H%M%S')"
OUTPUT_FILE="${OUTPUT_DIR}/faltante-evidence-${TIMESTAMP}.log"

print_header() {
  echo "=== Reporte de evidencia faltante ==="
  echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "Host: $(hostname 2>/dev/null || echo 'desconocido')"
  echo "Usuario: $(whoami 2>/dev/null || echo 'desconocido')"
  echo "Directorio del repo: ${REPO_ROOT}"
  if command -v ps >/dev/null 2>&1; then
    echo "Proceso PID 1: $(ps -p 1 -o comm= 2>/dev/null || echo 'desconocido')"
  fi
}

print_parameters() {
  echo
  echo "--- Parámetros utilizados ---"
  echo "FALTANTE_VALIDATE_HOST=${HOST}"
  echo "FALTANTE_VALIDATE_PORT=${PORT}"
  echo "FALTANTE_VALIDATE_TIMEOUT=${TIMEOUT}"
  echo "FALTANTE_KILL_PORT=${KILL_ON_CONFLICT}"
  echo "FALTANTE_SERVICE_NAME=${SERVICE_NAME}"
  echo "FALTANTE_JOURNAL_LINES=${JOURNAL_LINES}"
  echo "FALTANTE_EVIDENCE_DIR=${OUTPUT_DIR}"
}

run_validator() {
  echo
  echo "--- Resultado de validate_faltante.sh ---"
  (
    cd "${REPO_ROOT}"
    FALTANTE_VALIDATE_HOST="${HOST}" \
    FALTANTE_VALIDATE_PORT="${PORT}" \
    FALTANTE_VALIDATE_TIMEOUT="${TIMEOUT}" \
    FALTANTE_KILL_PORT="${KILL_ON_CONFLICT}" \
    FALTANTE_SERVICE_NAME="${SERVICE_NAME}" \
      "${VALIDATE_SCRIPT}"
  )
}

collect_journal() {
  echo
  echo "--- Últimos ${JOURNAL_LINES} eventos de journal (${SERVICE_NAME}.service) ---"
  if ! command -v journalctl >/dev/null 2>&1; then
    echo "journalctl no está disponible en este host."
    return
  fi
  if ! command -v systemctl >/dev/null 2>&1; then
    echo "systemd no está presente; no hay journal para la unidad solicitada."
    return
  fi
  if ! sudo journalctl -u "${SERVICE_NAME}.service" -n "${JOURNAL_LINES}"; then
    echo "No se pudieron obtener logs para ${SERVICE_NAME}.service (quizá la unidad no existe)."
  fi
}

main() {
  {
    print_header
    print_parameters
    run_validator
    collect_journal
    echo
    echo "=== Fin del reporte ==="
  } | tee "${OUTPUT_FILE}"
  echo "Evidencia guardada en ${OUTPUT_FILE}"
}

main "$@"
