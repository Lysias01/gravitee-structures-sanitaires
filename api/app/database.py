"""Accès à la base PostgreSQL (psycopg 3, requêtes paramétrées)."""
import math
import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "sante"),
    "user": os.getenv("DB_USER", "sante"),
    "password": os.getenv("DB_PASSWORD", "sante"),
    "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "3")),
}

TABLE = "structures_sanitaires"


@contextmanager
def get_conn():
    """Ouvre une connexion courte par requête (suffisant pour la démo)."""
    conn = psycopg.connect(**DB_CONFIG, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


def ping() -> bool:
    with get_conn() as conn:
        return conn.execute("SELECT 1 AS ok").fetchone()["ok"] == 1


def build_filters(q=None, type_=None, region=None, ville=None, statut=None):
    """Construit la clause WHERE à partir des critères fournis."""
    clauses, params = [], []
    if q:
        clauses.append("(nom ILIKE %s OR code ILIKE %s)")
        params += [f"%{q}%", f"%{q}%"]
    if type_:
        clauses.append("type = %s")
        params.append(type_)
    if region:
        clauses.append("lower(region) = lower(%s)")
        params.append(region)
    if ville:
        clauses.append("lower(ville) = lower(%s)")
        params.append(ville)
    if statut:
        clauses.append("statut = %s")
        params.append(statut)
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    return where, params


def paginate(where: str, params: list, page: int, size: int, order: str = "id ASC") -> dict:
    """Retourne une page de résultats + les métadonnées de pagination."""
    with get_conn() as conn:
        total = conn.execute(f"SELECT count(*) AS n FROM {TABLE} {where}", params).fetchone()["n"]
        rows = conn.execute(
            f"SELECT * FROM {TABLE} {where} ORDER BY {order} LIMIT %s OFFSET %s",
            [*params, size, (page - 1) * size],
        ).fetchall()
    return {
        "page": page,
        "size": size,
        "total": total,
        "pages": math.ceil(total / size) if total else 0,
        "rows": rows,
    }


def find_by_id(structure_id: int):
    with get_conn() as conn:
        return conn.execute(f"SELECT * FROM {TABLE} WHERE id = %s", [structure_id]).fetchone()
