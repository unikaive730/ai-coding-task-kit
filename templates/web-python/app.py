"""최소 웹 서비스 틀 (표준 라이브러리만, 설치 없음).

실행: python3 app.py · 주소 0.0.0.0:8000 (PORT 환경변수로 바꿈) · 미리보기 PORT 8000, URL /
API 더하기: 함수 (query, body) -> dict|list 를 만들고 ROUTES 에 '/api/이름' 으로 넣는다
화면: static/ 아래 파일. 캐시를 끄므로 고친 뒤 미리보기 새로고침만 하면 된다
"""
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")


def health(query, body):
    return {"ok": True}


ROUTES = {"/api/health": health}


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                      **{e: t + "; charset=utf-8" for e, t in {".html": "text/html", ".js": "text/javascript", ".css": "text/css",
                                                               ".json": "application/json", ".csv": "text/csv"}.items()}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _api(self, body):
        url = urlparse(self.path)
        fn = ROUTES.get(url.path)
        if fn is None:
            return False
        try:
            code, data = 200, fn({k: v[-1] for k, v in parse_qs(url.query).items()}, body)
        except Exception as e:  # 오류를 화면에서 바로 보이게
            code, data = 500, {"error": f"{type(e).__name__}: {e}"}
        raw = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
        return True

    def do_GET(self):
        if not self._api(None):
            super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        text = self.rfile.read(n).decode("utf-8") if n else ""
        try:
            body = json.loads(text) if text else None
        except json.JSONDecodeError:
            body = text
        if not self._api(body):
            self.send_error(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"serving on 0.0.0.0:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
