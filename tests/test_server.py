import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from receipt_ledger.server import ReceiptHandler


class ReceiptServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 绑定到 0 号端口让操作系统挑一个空闲端口,避免与本地服务冲突。
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), ReceiptHandler)
        host, port = cls.server.server_address
        cls.base = f"http://{host}:{port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_health_returns_ok(self):
        with urlopen(f"{self.base}/health") as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(json.loads(resp.read()), {"ok": True})

    def test_summary_returns_aggregated_totals(self):
        with urlopen(f"{self.base}/summary?path=data/sample_receipts.txt") as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read())

        self.assertEqual(data["food"]["CNY"], "49.70")
        self.assertEqual(data["software"]["USD"], "8.99")
        self.assertEqual(data["transport"]["CNY"], "4.00")

    def test_summary_filters_by_category(self):
        url = f"{self.base}/summary?path=data/sample_receipts.txt&category=food"
        with urlopen(url) as resp:
            data = json.loads(resp.read())

        self.assertEqual(list(data.keys()), ["food"])

    def test_summary_requires_path(self):
        with self.assertRaises(HTTPError) as cm:
            urlopen(f"{self.base}/summary")
        self.assertEqual(cm.exception.code, 400)

    def test_summary_returns_404_for_missing_file(self):
        with self.assertRaises(HTTPError) as cm:
            urlopen(f"{self.base}/summary?path=does-not-exist.txt")
        self.assertEqual(cm.exception.code, 404)

    def test_unknown_route_returns_404(self):
        with self.assertRaises(HTTPError) as cm:
            urlopen(f"{self.base}/whatever")
        self.assertEqual(cm.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
