"""Génère les contrats OpenAPI v1 et v2 à partir du code FastAPI.

Usage (depuis la racine du dépôt) :
    pip install -r api/requirements.txt pyyaml
    python scripts/export_openapi.py

Le contrat produit est enrichi pour Gravitee :
- `servers` pointe vers le backend sur le réseau Docker (utilisé comme endpoint à l'import) ;
- schéma de sécurité API Key (en-tête X-Gravitee-Api-Key) appliqué par la gateway ;
- erreurs ajoutées par la gateway : 401 (clé absente/invalide) et 429 (quota dépassé).
"""
import copy
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))

from app.main import app  # noqa: E402

GATEWAY_ERRORS = {
    "401": {
        "description": "Clé d'API absente, invalide ou souscription fermée (renvoyé par la gateway Gravitee)",
        "content": {"application/json": {"example": {"message": "Unauthorized", "http_status_code": 401}}},
    },
    "429": {
        "description": "Limite de requêtes ou quota du plan dépassé (renvoyé par la gateway Gravitee)",
        "content": {"application/json": {"example": {"message": "Rate limit exceeded ! You reach the limit of 5 requests per 10 seconds", "http_status_code": 429}}},
    },
}

VERSIONS = {
    "v1": {
        "title": "API Structures sanitaires",
        "version": "1.0.0",
        "server": "http://structures-api:8000/api/v1",
        "description": (
            "Version 1 : consultation, recherche et pagination d'un référentiel fictif de structures sanitaires.\n\n"
            "Accès via la gateway Gravitee : `http://localhost:8082/sante/structures/v1` avec l'en-tête "
            "`X-Gravitee-Api-Key`.\n\n"
            "Toutes les erreurs du backend suivent le format `ErrorResponse` (status, code, message, details)."
        ),
    },
    "v2": {
        "title": "API Structures sanitaires",
        "version": "2.0.0",
        "server": "http://structures-api:8000/api/v2",
        "description": (
            "Version 2 : ajoute statut, nombre de lits, téléphone, services et date d'ouverture, regroupe "
            "région et ville dans `localisation`, ajoute le filtre `statut` et le tri `tri`.\n\n"
            "Accès via la gateway Gravitee : `http://localhost:8082/sante/structures/v2` avec l'en-tête "
            "`X-Gravitee-Api-Key`."
        ),
    },
}


def refs(node):
    """Renvoie les noms de schémas référencés dans un fragment OpenAPI."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                yield v.rsplit("/", 1)[-1]
            else:
                yield from refs(v)
    elif isinstance(node, list):
        for v in node:
            yield from refs(v)


def used_schemas(paths: dict, schemas: dict) -> dict:
    """Ne garde que les schémas utilisés par les routes de la version."""
    keep, todo = set(), list(refs(paths))
    while todo:
        name = todo.pop()
        if name not in keep and name in schemas:
            keep.add(name)
            todo.extend(refs(schemas[name]))
    return {k: v for k, v in schemas.items() if k in keep}


def build(version: str) -> dict:
    spec = copy.deepcopy(app.openapi())
    conf = VERSIONS[version]
    prefix = f"/api/{version}"
    spec["info"] = {
        "title": conf["title"],
        "version": conf["version"],
        "description": conf["description"],
        "contact": {"name": "SI Groupe 2 — IBAM 2026"},
    }
    spec["servers"] = [{"url": conf["server"], "description": "Backend (réseau Docker, cible de la gateway)"}]
    paths = {}
    for path, item in spec["paths"].items():
        if not path.startswith(prefix):
            continue
        for op in item.values():
            op.pop("tags", None)
            op["tags"] = ["Structures sanitaires"]
            op["responses"].pop("422", None)
            op["responses"].update(copy.deepcopy(GATEWAY_ERRORS))
            op["security"] = [{"ApiKeyGravitee": []}]
        paths[path[len(prefix):]] = item
    spec["paths"] = paths
    spec["components"]["schemas"] = used_schemas(paths, spec["components"]["schemas"])
    spec["components"]["securitySchemes"] = {
        "ApiKeyGravitee": {"type": "apiKey", "in": "header", "name": "X-Gravitee-Api-Key"}
    }
    return spec


def main():
    out = ROOT / "openapi"
    out.mkdir(exist_ok=True)
    for version in VERSIONS:
        spec = build(version)
        target = out / f"structures-{version}.yaml"
        target.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"OK {target.relative_to(ROOT)} ({len(spec['paths'])} routes)")


if __name__ == "__main__":
    main()
