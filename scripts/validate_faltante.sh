#!/usr/bin/env bash
set -euo pipefail

HOST="${FALTANTE_VALIDATE_HOST:-127.0.0.1}"
PORT="${FALTANTE_VALIDATE_PORT:-8090}"
SERVICE_NAME="${FALTANTE_SERVICE_NAME:-faltante}"
TIMEOUT="${FALTANTE_VALIDATE_TIMEOUT:-5}"
KILL_ON_CONFLICT="${FALTANTE_KILL_PORT:-0}"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

check_systemd() {
  if ! command -v systemctl >/dev/null 2>&1; then
    log "systemd no está disponible; omitiendo verificación de unidad."
    return
  fi

  if ! systemctl list-unit-files >/dev/null 2>&1; then
    log "systemctl existe pero el init actual no es systemd; omitiendo verificación."
    return
  fi

  if [[ -f "/etc/systemd/system/${SERVICE_NAME}.service" ]] || systemctl list-unit-files "${SERVICE_NAME}.service" >/dev/null 2>&1; then
    log "Inspectando estado de ${SERVICE_NAME}.service via systemd"
    if ! sudo systemctl status --no-pager --full "${SERVICE_NAME}.service"; then
      log "Advertencia: systemctl status devolvió un error (servicio inactivo o fallando)."
    fi
  else
    log "systemctl disponible pero la unidad ${SERVICE_NAME}.service no está registrada en este host."
  fi
}

curl_endpoint() {
  local path="$1"
  local label="$2"
  local body_file
  body_file="$(mktemp)"
  local code_file="${body_file}.code"
  local url="http://${HOST}:${PORT}${path}"

  log "Ejecutando curl ${url}"
  if curl -sS --connect-timeout "${TIMEOUT}" -m "${TIMEOUT}" -o "${body_file}" -w "%{http_code}" "${url}" > "${code_file}"; then
    local http_code
    http_code="$(cat "${code_file}")"
    log "${label}: HTTP ${http_code}"
    if [[ "${http_code}" != "200" ]]; then
      log "Respuesta inesperada en ${label}: $(cat "${body_file}")"
    fi
  else
    local rc=$?
    local http_code="000"
    if [[ -s "${code_file}" ]]; then
      http_code="$(cat "${code_file}")"
    fi
    log "${label}: fallo curl (rc=${rc}, http=${http_code})."
    log "Mensaje: $(cat "${body_file}" 2>/dev/null || true)"
  fi
  rm -f "${body_file}" "${code_file}"
}

inspect_port() {
  log "Verificando si el puerto ${PORT} está en uso"
  local pids=""
  if command -v ss >/dev/null 2>&1; then
    pids=$(sudo ss -ltpn | awk -v port=":${PORT}" '$0 ~ port {match($0,/pid=([0-9]+)/,m); if (m[1] != "") print m[1]}') || true
  elif command -v lsof >/dev/null 2>&1; then
    pids=$(sudo lsof -ti TCP:"${PORT}" -sTCP:LISTEN || true)
  else
    log "Ni ss ni lsof están instalados; no se puede inspeccionar el puerto."
    return
  fi

  if [[ -z "${pids}" ]]; then
    log "No hay procesos escuchando en el puerto ${PORT}."
    return
  fi

  log "Procesos que usan el puerto ${PORT}: ${pids}"
  if [[ "${KILL_ON_CONFLICT}" == "1" ]]; then
    log "Finalizando procesos en conflicto (FALTANTE_KILL_PORT=1)"
    sudo kill -9 ${pids} || true
  fi
}

main() {
  log "=== Validación faltante (${SERVICE_NAME}) ==="
  check_systemd
  curl_endpoint "/" "Endpoint raíz"
  curl_endpoint "/healthz" "Endpoint health"
  inspect_port
  log "=== Validación completada ==="
}

main "$@"
