#!/usr/bin/env python3
"""Minimal HTTP service emulating faltante.service endpoints.

This module exposes two endpoints used throughout the operational
checklist:

- ``/`` returns a JSON payload describing the service status.
- ``/healthz`` returns a JSON payload with ``status: ok``.

The implementation intentionally avoids external dependencies so it can
run inside the container that lacks ``systemd``.  The handler is
thread-safe and logs basic request information to standard output,
helping operators validate that the fallback service is available when
``systemctl`` cannot be used.
"""
from __future__ import annotations

import argparse
import json
import logging
import signal
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional, Sequence, Tuple

LOG = logging.getLogger("faltante_service")


class RequestHandler(BaseHTTPRequestHandler):
    """Serve the minimal endpoints required for local validation."""

    server_version = "faltante/1.0"
    sys_version = ""

    # These attributes are mutated before the HTTP server starts so each
    # handler instance can access runtime configuration without relying on
    # global variables.
    service_name: str = "faltante"
    health_status: str = "ok"
    start_time: float = time.monotonic()

    def _send_json(self, payload: Dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - method name required by BaseHTTPRequestHandler
        LOG.info("Handling GET %s", self.path)
        if self.path == "/":
            uptime = max(0.0, time.monotonic() - self.start_time)
            self._send_json(
                {
                    "service": self.service_name,
                    "status": "running",
                    "uptime_seconds": round(uptime, 3),
                }
            )
        elif self.path == "/healthz":
            payload = {"service": self.service_name, "status": self.health_status}
            if self.health_status == "ok":
                self._send_json(payload)
            else:
                self._send_json(payload, status=HTTPStatus.SERVICE_UNAVAILABLE)
        else:
            self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: Tuple[Any, ...]) -> None:  # noqa: A003 - inherited signature
        LOG.info("%s - - %s", self.address_string(), format % args)


def create_server(host: str, port: int, *, service_name: str, health_status: str) -> HTTPServer:
    """Create a configured ``HTTPServer`` instance.

    Exposed as a helper so automated tests can instantiate the service
    without having to spawn the CLI entry point.
    """

    RequestHandler.service_name = service_name
    RequestHandler.health_status = health_status
    RequestHandler.start_time = time.monotonic()

    return HTTPServer((host, port), RequestHandler)


def run(host: str = "127.0.0.1", port: int = 8090, *, service_name: str, health_status: str) -> None:
    """Run the HTTP server until receiving SIGINT or SIGTERM."""

    server = create_server(host, port, service_name=service_name, health_status=health_status)
    shutdown_event = threading.Event()

    def _signal_handler(signum: int, _frame: Any) -> None:
        LOG.info("Received signal %s, shutting down.", signum)
        shutdown_event.set()
        server.shutdown()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    LOG.info(
        "Starting faltante fallback server on %s:%s (service=%s, health=%s)",
        host,
        port,
        service_name,
        health_status,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info("Keyboard interrupt received, shutting down")
    finally:
        shutdown_event.set()
        server.server_close()
        LOG.info("Server stopped")


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the fallback faltante HTTP service.")
    parser.add_argument("--host", default="127.0.0.1", help="Host/IP to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8090, help="Port to bind (default: 8090)")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging verbosity",
    )
    parser.add_argument("--service-name", default="faltante", help="Service name advertised in responses")
    parser.add_argument(
        "--health-status",
        default="ok",
        choices=["ok", "fail"],
        help="Health response status (fail => HTTP 503)",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="[%(asctime)s] %(levelname)s: %(message)s")
    run(host=args.host, port=args.port, service_name=args.service_name, health_status=args.health_status)


if __name__ == "__main__":
    main()
