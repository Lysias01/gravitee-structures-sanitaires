"""Modèles de données exposés (utilisés aussi pour générer le contrat OpenAPI)."""
from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TypeStructure(str, Enum):
    CHU = "CHU"
    CHR = "CHR"
    CMA = "CMA"
    CSPS = "CSPS"
    CLINIQUE = "CLINIQUE"


class Statut(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVE = "PRIVE"


class Tri(str, Enum):
    id = "id"
    nom = "nom"
    nom_desc = "-nom"
    lits = "lits"
    lits_desc = "-lits"


# ---------- Erreurs ----------
class ErrorDetail(BaseModel):
    champ: str = Field(..., examples=["size"])
    message: str = Field(..., examples=["Input should be less than or equal to 100"])


class ErrorResponse(BaseModel):
    status: int = Field(..., examples=[404])
    code: str = Field(..., examples=["STRUCTURE_NOT_FOUND"])
    message: str = Field(..., examples=["Aucune structure avec l'id 999"])
    details: List[ErrorDetail] = []


# ---------- Version 1 ----------
class StructureV1(BaseModel):
    id: int = Field(..., examples=[1])
    code: str = Field(..., examples=["CHU-CEN-001"])
    nom: str = Field(..., examples=["CHU Fictif de Ouagadougou Nord"])
    type: TypeStructure
    region: str = Field(..., examples=["Centre"])
    ville: str = Field(..., examples=["Ouagadougou"])


class PageV1(BaseModel):
    page: int = Field(..., examples=[1])
    size: int = Field(..., examples=[10])
    total: int = Field(..., examples=[40])
    pages: int = Field(..., examples=[4])
    items: List[StructureV1]


# ---------- Version 2 ----------
class Localisation(BaseModel):
    region: str = Field(..., examples=["Centre"])
    ville: str = Field(..., examples=["Ouagadougou"])


class StructureV2(BaseModel):
    id: int = Field(..., examples=[1])
    code: str = Field(..., examples=["CHU-CEN-001"])
    nom: str = Field(..., examples=["CHU Fictif de Ouagadougou Nord"])
    type: TypeStructure
    statut: Statut
    localisation: Localisation
    nombre_lits: int = Field(..., examples=[620])
    telephone: Optional[str] = Field(None, examples=["+226 25 00 10 01"])
    services: List[str] = Field(..., examples=[["urgences", "maternite"]])
    date_ouverture: Optional[date] = None


class PageV2(BaseModel):
    page: int
    size: int
    total: int
    pages: int
    items: List[StructureV2]


class Health(BaseModel):
    status: str = Field(..., examples=["UP"])
    database: str = Field(..., examples=["UP"])
    version: str = Field(..., examples=["1.0.0"])
