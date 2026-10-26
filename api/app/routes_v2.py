"""Version 2 de l'API.

Évolutions par rapport à la v1 (changement non rétrocompatible → nouvelle version) :
- la région et la ville sont regroupées dans un objet `localisation` ;
- nouveaux champs : statut, nombre_lits, telephone, services, date_ouverture ;
- nouveau filtre `statut` et paramètre de tri `tri`.
"""
from typing import Optional

from fastapi import APIRouter, Path, Query

from . import database as db
from .errors import ApiError
from .schemas import ErrorResponse, PageV2, Statut, StructureV2, Tri, TypeStructure

router = APIRouter(prefix="/api/v2", tags=["Structures sanitaires v2"])

ERRORS = {
    400: {"model": ErrorResponse, "description": "Paramètres invalides (VALIDATION_ERROR, MISSING_CRITERIA)"},
    503: {"model": ErrorResponse, "description": "Base de données indisponible (DATABASE_UNAVAILABLE)"},
    500: {"model": ErrorResponse, "description": "Erreur interne (INTERNAL_ERROR)"},
}

ORDER_BY = {
    "id": "id ASC",
    "nom": "nom ASC",
    "-nom": "nom DESC",
    "lits": "nombre_lits ASC",
    "-lits": "nombre_lits DESC",
}


def to_v2(row: dict) -> dict:
    return {
        "id": row["id"],
        "code": row["code"],
        "nom": row["nom"],
        "type": row["type"],
        "statut": row["statut"],
        "localisation": {"region": row["region"], "ville": row["ville"]},
        "nombre_lits": row["nombre_lits"],
        "telephone": row["telephone"],
        "services": row["services"],
        "date_ouverture": row["date_ouverture"],
    }


def page_v2(result: dict) -> dict:
    rows = result.pop("rows")
    return {**result, "items": [to_v2(r) for r in rows]}


@router.get("/structures", response_model=PageV2, summary="Lister les structures (paginé, triable)", responses=ERRORS)
def list_structures(
    page: int = Query(1, ge=1, description="Numéro de page, à partir de 1"),
    size: int = Query(10, ge=1, le=100, description="Nombre d'éléments par page (1 à 100)"),
    tri: Tri = Query(Tri.id, description="Tri : id, nom, -nom, lits, -lits"),
):
    return page_v2(db.paginate("", [], page, size, ORDER_BY[tri.value]))


@router.get(
    "/structures/search",
    response_model=PageV2,
    summary="Rechercher des structures (paginé, triable)",
    description="Au moins un critère est obligatoire. Nouveau en v2 : filtre `statut`.",
    responses=ERRORS,
)
def search_structures(
    q: Optional[str] = Query(None, min_length=2, max_length=100, description="Texte recherché dans le nom ou le code"),
    type: Optional[TypeStructure] = Query(None),
    statut: Optional[Statut] = Query(None, description="PUBLIC ou PRIVE"),
    region: Optional[str] = Query(None, max_length=60),
    ville: Optional[str] = Query(None, max_length=80),
    tri: Tri = Query(Tri.id),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    if not any([q, type, statut, region, ville]):
        raise ApiError(400, "MISSING_CRITERIA", "Fournir au moins un critère : q, type, statut, region ou ville")
    where, params = db.build_filters(
        q, type.value if type else None, region, ville, statut.value if statut else None
    )
    return page_v2(db.paginate(where, params, page, size, ORDER_BY[tri.value]))


@router.get(
    "/structures/{id}",
    response_model=StructureV2,
    summary="Obtenir le détail complet d'une structure",
    responses={404: {"model": ErrorResponse, "description": "Structure inexistante (STRUCTURE_NOT_FOUND)"}, **ERRORS},
)
def get_structure(id: int = Path(..., ge=1, description="Identifiant technique de la structure")):
    row = db.find_by_id(id)
    if row is None:
        raise ApiError(404, "STRUCTURE_NOT_FOUND", f"Aucune structure avec l'id {id}")
    return to_v2(row)
