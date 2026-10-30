// 최소 웹 서비스 틀 (Node 내장 모듈만, 설치 없음)
// 실행: node server.js · 주소 0.0.0.0:3000 (PORT 환경변수로 바꿈) · 미리보기 PORT 3000, URL /
// API 더하기: (query, body) => 객체 를 만들어 ROUTES 에 '/api/이름' 으로 넣는다
// 화면: public/ 아래 파일. 캐시를 끄므로 고친 뒤 미리보기 새로고침만 하면 된다
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = Number(process.env.PORT || 3000);
const PUBLIC = path.join(__dirname, 'public');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.csv': 'text/csv; charset=utf-8' };

const ROUTES = {
  '/api/health': () => ({ ok: true }),
};

function send(res, code, type, buf) {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(buf);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const fn = ROUTES[url.pathname];
  if (fn) {
    let raw = '';
    req.on('data', (c) => { raw += c; });
    req.on('end', async () => {
      try {
        let body = raw;
        try { body = raw ? JSON.parse(raw) : null; } catch { /* 글자 그대로 */ }
        const data = await fn(Object.fromEntries(url.searchParams), body);
        send(res, 200, TYPES['.json'], JSON.stringify(data));
      } catch (e) {
        send(res, 500, TYPES['.json'], JSON.stringify({ error: String(e) }));
      }
    });
    return;
  }
  const rel = url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname.slice(1));
  const file = path.normalize(path.join(PUBLIC, rel));
  if (!file.startsWith(PUBLIC)) return send(res, 403, TYPES['.json'], '{"error":"forbidden"}');
  fs.readFile(file, (err, buf) => {
    if (err) return send(res, 404, TYPES['.json'], '{"error":"not found"}');
    send(res, 200, TYPES[path.extname(file)] || 'application/octet-stream', buf);
  });
});

server.listen(PORT, '0.0.0.0', () => console.log(`serving on 0.0.0.0:${PORT}`));
