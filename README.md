# Gestion du cycle de vie d'une API avec Gravitee API Management

**Projet Développement à base de composants et services web — IBAM 2026**
**Thème 22 · SI Groupe 2**

Une API REST de consultation des structures sanitaires (données fictives) est développée avec FastAPI, puis exposée, sécurisée et gérée tout au long de son cycle de vie avec Gravitee APIM 4.x : routage, contrat OpenAPI, plan avec authentification et quota, application consommatrice et souscription, publication, retrait, arrêt technique et passage à une version 2.

## Équipe

| Membre | Rôle |
|---|---|
| SIMPORE Wend-Yam Lysias Eldad | Chef de projet, architecture, installation Docker |
| KAZIENGA Eva Benjamine | API FastAPI, base de données, données fictives |
| NANA Florent Kyêsba Rodrigue | Contrat OpenAPI, catalogue des erreurs |
| YAMEOGO Fiacre Donald Tebnooma | Gravitee : enregistrement, routage, plans, quota, souscriptions |
| OUEDRAOGO D. Adan Franck | Cycle de vie, version 2, tests Postman/Newman |

## Architecture

```
                    ┌──────────────────────── Gravitee APIM 4.x ────────────────────────┐
 Consommateur ───►  │  Gateway :8082  (plan API Key, rate limit 5 req/10 s, quota 1000/j) │ ───► API FastAPI :8000 ───► PostgreSQL :5433
 (Postman, app)     │                                                                    │      /api/v1, /api/v2      (base de référence)
       │            │  Management API :8083 ◄── Console :8084 (administration)           │
       └──────────► │  Portail développeur :8085 (découverte, souscription, clé d'API)   │
                    │  MongoDB (configuration) · Elasticsearch (analytique)              │
                    └────────────────────────────────────────────────────────────────────┘
```

Le consommateur obtient une clé sur le portail puis appelle uniquement la gateway, qui vérifie la clé et le quota avant de transmettre la requête au backend.

## Contenu du dépôt

| Dossier / fichier | Contenu |
|---|---|
| `docker-compose.yml`, `.env.example` | Gravitee + PostgreSQL + API, installation en une commande |
| `api/` | Code FastAPI (v1 et v2), `Dockerfile`, `requirements.txt` |
| `db/init/` | `01_schema.sql` (création), `02_seed.sql` (40 structures fictives) |
| `openapi/` | Contrats `structures-v1.yaml` et `structures-v2.yaml` |
| `gravitee/` | Procédure de configuration Gravitee pas à pas + exports JSON des API |
| `tests/postman/` | Collection et environnement Postman |
| `tests/resultats/` | Résultats Newman attendus |
| `docs/erreurs.md` | Catalogue des erreurs (backend et gateway) |
| `scripts/` | Génération OpenAPI, démonstration du quota |
| `presentation/` | Présentation PowerPoint |

## Prérequis

- Docker Desktop (ou Docker Engine + Compose v2) avec **au moins 6 Go de RAM** alloués (8 Go conseillés).
- Ports libres : 8000, 8082, 8083, 8084, 8085, 5433.
- Postman, et Node.js 18+ pour Newman (`npm install -g newman`).
- Sous Linux uniquement, pour Elasticsearch : `sudo sysctl -w vm.max_map_count=262144`.

## Installation

```bash
git clone https://github.com/<compte>/gravitee-structures-sanitaires.git
cd gravitee-structures-sanitaires
cp .env.example .env          # Windows PowerShell : copy .env.example .env
docker compose up -d --build
docker compose ps             # attendre que tous les services soient "running" / "healthy" (1 à 3 min)
```

Vérifications :

| URL | Attendu |
|---|---|
| http://localhost:8000/health | `{"status":"UP","database":"UP",...}` |
| http://localhost:8000/docs | Swagger de l'API |
| http://localhost:8084 | Console Gravitee (admin / admin) |
| http://localhost:8085 | Portail développeur |

La base est créée et remplie automatiquement au premier démarrage (scripts de `db/init/`).

Ensuite, configurer Gravitee en suivant **[gravitee/README.md](gravitee/README.md)** (import de l'API, plans, application, souscription, cycle de vie, version 2), ou importer directement les exports JSON du dossier `gravitee/`.

## API

| Route (via la gateway : `http://localhost:8082/sante/structures/v1`) | Description |
|---|---|
| `GET /structures?page=1&size=10` | Liste paginée |
| `GET /structures/search?q=&type=&region=&ville=` | Recherche paginée (au moins un critère) |
| `GET /structures/{id}` | Détail |

La v2 (`/sante/structures/v2`) regroupe région et ville dans `localisation`, ajoute statut, nombre de lits, téléphone, services, date d'ouverture, le filtre `statut` et le tri `tri` (`nom`, `-nom`, `lits`, `-lits`).

Toutes les requêtes via la gateway exigent l'en-tête `X-Gravitee-Api-Key`. Format et liste des erreurs : [docs/erreurs.md](docs/erreurs.md).
### Pagination

Les listes de resultats prennent en charge la pagination via deux parametres de requete optionnels :
• page : L index de la page a recuperer (1 par defaut).
• size : Le nombre d elements par page (10 par defaut, avec une limite maximale de 100).
Chaque reponse paginee retourne un objet contenant les proprietes suivantes :
• page : La page courante.
• size : La taille de la page.
• total : Le nombre total d elements disponibles.
• pages : Le nombre total de pages (calcule selon la formule : total divise par size, arrondi a l entier superieur).
• items : Le tableau des donnees de la page actuelle.
Exemple concret :
On prend Une requete sur GET /structures?page=2&size=5 pour un ensemble de 40 structures au total retournera un resultat reparti sur 8 pages. Cette deuxieme page affichera specifiquement les structures correspondantes aux identifiants 6 a 10.

## Tests

1. Importer `tests/postman/collection.json` et `tests/postman/environment.json` dans Postman.
2. Renseigner `api_key` (et `api_key_v2`) avec les clés obtenues par souscription.
3. Lancer en ligne de commande :

```bash
newman run tests/postman/collection.json -e tests/postman/environment.json \
  --env-var api_key=<clé_v1> --env-var api_key_v2=<clé_v2> \
  --folder "1. Backend direct" --folder "2. Gateway Gravitee - accès et quota" --folder "3. Gateway Gravitee - version 2"
```

| Dossier | Ce qui est vérifié |
|---|---|
| 1. Backend direct | Santé, pagination, recherche, détail, erreurs 400/404/405, format v2 |
| 2. Gateway — accès et quota | 401 sans clé ou clé invalide, **scénario de bout en bout** (clé → gateway → API → base : la ligne `CHU-CEN-001` du seed est retrouvée), 429 au-delà de 5 req / 10 s |
| 3. Gateway — version 2 | Accès à la v2 avec sa propre souscription |
| 4. Cycle de vie (manuel) | 200 après retrait de publication, refus après arrêt technique |

Les résultats de référence sont dans `tests/resultats/`.

Régénérer les contrats OpenAPI après une modification du code :

```bash
pip install -r api/requirements.txt pyyaml
python scripts/export_openapi.py
```

## Arrêt et réinitialisation

```bash
docker compose down        # arrêt, données conservées
docker compose down -v     # arrêt et suppression des volumes (repart de zéro)
```
