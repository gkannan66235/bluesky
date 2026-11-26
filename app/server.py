"""bluesky: tiny HTTP demo app for the kagent GitOps demo (stdlib only).

  GET /          greeting (APP_MESSAGE) + version
  GET /healthz   liveness/readiness
  GET /alloc?mb=N  allocate N MiB and hold it (demo: trigger OOMKilled under a low memory limit)
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

VERSION = os.environ.get("APP_VERSION", "dev")
MESSAGE = os.environ.get("APP_MESSAGE", "Hello from bluesky")
_held = []  # keeps /alloc memory referenced


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/healthz":
            return self._send(200, {"status": "ok"})
        if url.path == "/alloc":
            mb = min(int(parse_qs(url.query).get("mb", ["64"])[0]), 4096)
            _held.append(bytearray(mb * 1024 * 1024))
            return self._send(200, {"allocated_mb": mb, "held_chunks": len(_held)})
        if url.path == "/":
            return self._send(200, {"message": MESSAGE, "version": VERSION})
        self._send(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
