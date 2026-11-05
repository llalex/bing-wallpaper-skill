import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import wallpaper


class WallpaperClientTest(unittest.TestCase):
    def test_cli_handles_local_http_responses(self):
        cases = [
            (404, {}, b'{"msg":"Missing today"}', "today", 1,
             {"code": 404, "msg": "Missing today", "data": None}),
            (429, {"Retry-After": "30"}, b"Too many requests", "today", 1,
             {"code": 429, "msg": "Too Many Requests", "data": None, "retry_after": 30}),
            (503, {"Retry-After": "10"}, b'{"msg":"Search busy"}', "search", 1,
             {"code": 503, "msg": "Search busy", "data": None, "retry_after": 10}),
            (200, {}, b'{"code":0,"data":{"sort":"relevance","strategy":"keyword","wallpapers":[]}}',
             "search", 0, {"code": 0, "data": {"sort": "relevance", "strategy": "keyword", "wallpapers": []}}),
            (200, {}, b"<html>Upstream error</html>", "today", 1,
             {"code": 502, "msg": "Invalid wallpaper service response", "data": None}),
        ]

        for status, headers, body, operation, exit_code, expected in cases:
            with self.subTest(status=status, operation=operation, expected_code=expected["code"]):
                requests = []

                class Handler(BaseHTTPRequestHandler):
                    def do_GET(self):
                        requests.append(urlsplit(self.path).path)
                        self.send_response(status)
                        for name, value in headers.items():
                            self.send_header(name, value)
                        self.end_headers()
                        self.wfile.write(body)

                    def log_message(self, *args):
                        pass

                with HTTPServer(("127.0.0.1", 0), Handler) as server:
                    worker = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
                    worker.start()
                    try:
                        args = [operation, "--base-url", "http://127.0.0.1:{}".format(server.server_port)]
                        if operation == "search":
                            args.extend(["--query", "太阳"])
                        out = io.StringIO()
                        with redirect_stdout(out):
                            self.assertEqual(exit_code, wallpaper.main(args))
                        self.assertEqual(expected, json.loads(out.getvalue()))
                        self.assertEqual(["/api/v1/wallpapers/" + operation], requests)
                    finally:
                        server.shutdown()
                        worker.join()

    def test_search_passes_unicode_query_recency_and_limit(self):
        out = io.StringIO()
        with patch.object(wallpaper, "fetch", return_value={"code": 0, "msg": "success", "data": {"sort": "recent", "wallpapers": []}}) as fetch:
            with redirect_stdout(out):
                self.assertEqual(0, wallpaper.main(["search", "--query", "雪山 湖泊", "--sort", "recent", "--limit", "10"]))
        request = urlsplit(fetch.call_args[0][0])
        self.assertEqual("/api/v1/wallpapers/search", request.path)
        self.assertEqual({"q": ["雪山 湖泊"], "sort": ["recent"], "limit": ["10"]}, parse_qs(request.query))
        self.assertEqual([], json.loads(out.getvalue())["data"]["wallpapers"])

    def test_rate_limit_reports_retry_after_without_retrying(self):
        error = HTTPError("https://bing.plmeizi.com", 429, "limit", {"Retry-After": "30"}, io.BytesIO(b"nginx"))
        out = io.StringIO()
        with patch.object(wallpaper, "fetch", side_effect=error) as fetch:
            with redirect_stdout(out):
                self.assertEqual(1, wallpaper.main(["today"]))
        self.assertEqual(429, json.loads(out.getvalue())["code"])
        self.assertEqual(30, json.loads(out.getvalue())["retry_after"])
        fetch.assert_called_once()

    def test_today_not_updated_does_not_fetch_recent(self):
        error = HTTPError("https://bing.plmeizi.com", 404, "missing", {}, io.BytesIO(b'{"code":404,"msg":"Missing today","data":null}'))
        out = io.StringIO()
        with patch.object(wallpaper, "fetch", side_effect=error) as fetch:
            with redirect_stdout(out):
                self.assertEqual(1, wallpaper.main(["today", "--resolution", "portrait"]))
        self.assertEqual(404, json.loads(out.getvalue())["code"])
        fetch.assert_called_once()
