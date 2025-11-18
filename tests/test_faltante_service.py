"""Regression tests for the fallback faltante HTTP service."""
from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
import unittest

from scripts import faltante_service


class FaltanteServiceTestCase(unittest.TestCase):
    def _start_server(self, **kwargs):
        server = faltante_service.create_server("127.0.0.1", 0, **kwargs)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        # Ensure the server has time to bind before issuing requests.
        time.sleep(0.05)
        return server, thread, server.server_address[1]

    def _stop_server(self, server, thread):
        server.shutdown()
        thread.join(timeout=1)
        server.server_close()

    def test_root_endpoint_reports_service_metadata(self):
        server, thread, port = self._start_server(service_name="qa-faltante", health_status="ok")
        try:
            response = urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2)
            payload = json.loads(response.read().decode("utf-8"))
            self.assertEqual(payload["service"], "qa-faltante")
            self.assertEqual(payload["status"], "running")
            self.assertGreaterEqual(payload["uptime_seconds"], 0)
        finally:
            self._stop_server(server, thread)

    def test_health_endpoint_returns_200_when_healthy(self):
        server, thread, port = self._start_server(service_name="qa-faltante", health_status="ok")
        try:
            response = urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=2)
            payload = json.loads(response.read().decode("utf-8"))
            self.assertEqual(payload, {"service": "qa-faltante", "status": "ok"})
        finally:
            self._stop_server(server, thread)

    def test_health_endpoint_returns_503_when_forced_to_fail(self):
        server, thread, port = self._start_server(service_name="qa-faltante", health_status="fail")
        try:
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=2)
            self.assertEqual(ctx.exception.code, 503)
        finally:
            self._stop_server(server, thread)


if __name__ == "__main__":
    unittest.main()
