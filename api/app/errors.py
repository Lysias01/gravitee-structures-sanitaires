"""Format d'erreur unique de l'API et gestionnaires d'exceptions.

Toutes les erreurs renvoient le même corps JSON :
    {"status": 404, "code": "STRUCTURE_NOT_FOUND", "message": "...", "details": [...]}
"""
import logging

import psycopg
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

log = logging.getLogger("structures-api")


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, details=None):
        self.status, self.code, self.message, self.details = status, code, message, details or []


def error_body(status: int, code: str, message: str, details=None) -> dict:
    return {"status": status, "code": code, "message": message, "details": details or []}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def api_error(_: Request, exc: ApiError):
        return JSONResponse(status_code=exc.status, content=error_body(exc.status, exc.code, exc.message, exc.details))

    @app.exception_handler(RequestValidationError)
    async def validation_error(_: Request, exc: RequestValidationError):
        details = [
            {"champ": ".".join(str(p) for p in e["loc"][1:]) or str(e["loc"][0]), "message": e["msg"]}
            for e in exc.errors()
        ]
        return JSONResponse(status_code=400, content=error_body(400, "VALIDATION_ERROR", "Paramètres invalides", details))

    @app.exception_handler(StarletteHTTPException)
    async def http_error(_: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return JSONResponse(status_code=404, content=error_body(404, "ROUTE_NOT_FOUND", "Ressource inexistante"))
        if exc.status_code == 405:
            return JSONResponse(status_code=405, content=error_body(405, "METHOD_NOT_ALLOWED", "Méthode non autorisée (API en lecture seule)"))
        return JSONResponse(status_code=exc.status_code, content=error_body(exc.status_code, "HTTP_ERROR", str(exc.detail)))

    @app.exception_handler(psycopg.OperationalError)
    async def db_down(_: Request, exc: psycopg.OperationalError):
        log.error("Base de données indisponible : %s", exc)
        return JSONResponse(status_code=503, content=error_body(503, "DATABASE_UNAVAILABLE", "Base de données indisponible, réessayez plus tard"))

    @app.exception_handler(Exception)
    async def unexpected(_: Request, exc: Exception):
        log.exception("Erreur inattendue")
        return JSONResponse(status_code=500, content=error_body(500, "INTERNAL_ERROR", "Erreur interne du serveur"))
