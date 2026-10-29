"""최소 웹 서비스 틀 (FastAPI).

실행: pip install -r requirements.txt && python app.py
주소: 0.0.0.0:8000 (PORT 환경변수로 바꿈) · 미리보기에서 PORT 8000, URL /
"""
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="service")


@app.get("/api/health")
def health():
    return {"ok": True}


app.mount("/static", StaticFiles(directory=os.path.join(BASE, "static")), name="static")


@app.get("/")
def index():
    return FileResponse(os.path.join(BASE, "static", "index.html"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"serving on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
