from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .cli import DecimalEncoder, summarize_file


class ReceiptHandler(BaseHTTPRequestHandler):
    """把收据汇总能力暴露为只读 HTTP 接口,使容器可以监听端口接受质检访问。"""

    def do_GET(self) -> None:
        parsed = urlsplit(self.path)
        if parsed.path == "/health":
            self._send_json(200, {"ok": True})
            return
        if parsed.path == "/summary":
            self._handle_summary(parsed.query)
            return
        self._send_json(404, {"error": "not found"})

    def _handle_summary(self, query: str) -> None:
        params = parse_qs(query)
        raw_path = (params.get("path") or [""])[0].strip()
        if not raw_path:
            self._send_json(400, {"error": "path is required"})
            return
        path = Path(raw_path)
        if not path.is_file():
            self._send_json(404, {"error": f"file not found: {raw_path}"})
            return
        category = (params.get("category") or [None])[0]
        try:
            totals = summarize_file(path, category)
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
            return
        self._send_json(200, totals)

    def _send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, cls=DecimalEncoder, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        # 测试和质检都用日志噪音很高,简化为单行 stderr 输出。
        return


def serve(host: str = "0.0.0.0", port: int | None = None) -> None:
    resolved_port = int(os.environ.get("PORT", "8788")) if port is None else port
    server = ThreadingHTTPServer((host, resolved_port), ReceiptHandler)
    print(f"receipt-ledger listening on {resolved_port}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
