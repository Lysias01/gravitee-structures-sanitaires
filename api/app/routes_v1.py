"""Version 1 de l'API : lecture, recherche et pagination (champs de base)."""
from typing import Optional

from fastapi import APIRouter, Path, Query

from . import database as db
from .errors import ApiError
from .schemas import ErrorResponse, PageV1, StructureV1, TypeStructure

router = APIRouter(prefix="/api/v1", tags=["Structures sanitaires v1"])

ERRORS = {
    400: {"model": ErrorResponse, "description": "Paramètres invalides (VALIDATION_ERROR, MISSING_CRITERIA)"},
    503: {"model": ErrorResponse, "description": "Base de données indisponible (DATABASE_UNAVAILABLE)"},
    500: {"model": ErrorResponse, "description": "Erreur interne (INTERNAL_ERROR)"},
}


def to_v1(row: dict) -> dict:
    return {k: row[k] for k in ("id", "code", "nom", "type", "region", "ville")}


def page_v1(result: dict) -> dict:
    rows = result.pop("rows")
    return {**result, "items": [to_v1(r) for r in rows]}


@router.get(
    "/structures",
    response_model=PageV1,
    summary="Lister les structures (paginé)",
    responses=ERRORS,
)
def list_structures(
    page: int = Query(1, ge=1, description="Numéro de page, à partir de 1"),
    size: int = Query(10, ge=1, le=100, description="Nombre d'éléments par page (1 à 100)"),
):
    return page_v1(db.paginate("", [], page, size))


@router.get(
    "/structures/search",
    response_model=PageV1,
    summary="Rechercher des structures (paginé)",
    description="Au moins un critère est obligatoire. `q` cherche dans le nom et le code.",
    responses=ERRORS,
)
def search_structures(
    q: Optional[str] = Query(None, min_length=2, max_length=100, description="Texte recherché dans le nom ou le code"),
    type: Optional[TypeStructure] = Query(None, description="Type de structure"),
    region: Optional[str] = Query(None, max_length=60, description="Région (insensible à la casse)"),
    ville: Optional[str] = Query(None, max_length=80, description="Ville (insensible à la casse)"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    if not any([q, type, region, ville]):
        raise ApiError(400, "MISSING_CRITERIA", "Fournir au moins un critère : q, type, region ou ville")
    where, params = db.build_filters(q, type.value if type else None, region, ville)
    return page_v1(db.paginate(where, params, page, size))


@router.get(
    "/structures/{id}",
    response_model=StructureV1,
    summary="Obtenir le détail d'une structure",
    responses={404: {"model": ErrorResponse, "description": "Structure inexistante (STRUCTURE_NOT_FOUND)"}, **ERRORS},
)
def get_structure(id: int = Path(..., ge=1, description="Identifiant technique de la structure")):
    row = db.find_by_id(id)
    if row is None:
        raise ApiError(404, "STRUCTURE_NOT_FOUND", f"Aucune structure avec l'id {id}")
    return to_v1(row)
