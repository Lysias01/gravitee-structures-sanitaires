"""API REST de consultation des structures sanitaires (données fictives).

Backend exposé derrière Gravitee API Management.
Lancement local : uvicorn app.main:app --reload --port 8000
"""
import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse

from . import database as db
from .errors import register_error_handlers
from .routes_v1 import router as v1
from .routes_v2 import router as v2
from .schemas import Health

API_VERSION = "2.0.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("structures-api")

app = FastAPI(
    title="API Structures sanitaires",
    version=API_VERSION,
    description="Consultation, recherche et pagination d'un référentiel fictif de structures sanitaires. "
    "Projet IBAM 2026 — Thème 22 — SI Groupe 2.",
)
register_error_handlers(app)
app.include_router(v1)
app.include_router(v2)


@app.middleware("http")
async def correlation_and_logs(request: Request, call_next):
    """Propage un identifiant de corrélation et journalise chaque requête."""
    cid = request.headers.get("X-Correlation-ID") or request.headers.get("X-Gravitee-Request-Id") or str(uuid.uuid4())
    start = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000
    response.headers["X-Correlation-ID"] = cid
    log.info("%s %s -> %s (%.1f ms) cid=%s", request.method, request.url.path, response.status_code, duration, cid)
    return response


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.get("/health", response_model=Health, tags=["Supervision"], summary="État du service et de la base")
def health():
    try:
        db.ping()
        return {"status": "UP", "database": "UP", "version": API_VERSION}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "DEGRADED", "database": "DOWN", "version": API_VERSION})
