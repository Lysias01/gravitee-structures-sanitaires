# Catalogue des erreurs

Toutes les erreurs du backend ont le même corps JSON :

```json
{
  "status": 400,
  "code": "VALIDATION_ERROR",
  "message": "Paramètres invalides",
  "details": [{ "champ": "size", "message": "Input should be less than or equal to 100" }]
}
```

## Erreurs renvoyées par le backend (FastAPI)

| HTTP | Code | Quand | Exemple de requête |
|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Paramètre mal typé ou hors limites (`page` < 1, `size` > 100, `id` non numérique, `type` ou `statut` inconnu, `q` < 2 caractères) | `GET /structures?size=500` |
| 400 | `MISSING_CRITERIA` | Recherche sans aucun critère | `GET /structures/search` |
| 404 | `STRUCTURE_NOT_FOUND` | Identifiant inexistant | `GET /structures/999` |
| 404 | `ROUTE_NOT_FOUND` | Chemin inexistant | `GET /inconnu` |
| 405 | `METHOD_NOT_ALLOWED` | Écriture tentée sur l'API (lecture seule) | `DELETE /structures/1` |
| 503 | `DATABASE_UNAVAILABLE` | PostgreSQL injoignable | `docker stop structures_db` puis un appel |
| 500 | `INTERNAL_ERROR` | Erreur imprévue (détail uniquement dans les journaux) | — |

`GET /health` renvoie `200 {"status":"UP","database":"UP"}` ou `503 {"status":"DEGRADED","database":"DOWN"}`.

## Erreurs ajoutées par la gateway Gravitee

| HTTP | Cause | Comment la provoquer |
|---|---|---|
| 401 | En-tête `X-Gravitee-Api-Key` absent, clé inconnue ou souscription fermée | Appel sans en-tête |
| 429 | Limite du plan dépassée (5 req / 10 s) ou quota journalier atteint (1 000 req) | `scripts/test-quota.sh <clé>` |
| 404 | API arrêtée (*Stop the API*) ou context path inexistant | Arrêter l'API puis l'appeler |

## Traçabilité

Chaque réponse du backend porte un en-tête `X-Correlation-ID` (repris de `X-Gravitee-Request-Id` quand l'appel passe par la gateway), et chaque requête est journalisée avec sa méthode, son chemin, son code HTTP et sa durée : `docker logs structures_api`.

### Exemple 1 : structure inexistante

Requête : GET /api/v1/structures/999

L'identifiant 999 n'existe pas dans la base, l'API répond *404* :

json
{
  "status": 404,
  "code": "STRUCTURE_NOT_FOUND",
  "message": "Aucune structure avec l'id 999",
  "details": []
}


### Exemple 2 : paramètre invalide

Requête : GET /api/v1/structures?size=500

La taille de page est limitée à 100, l'API répond *400* et indique le champ en cause dans details :

json
{
  "status": 400,
  "code": "VALIDATION_ERROR",
  "message": "Paramètres invalides",
  "details": [
    { "champ": "size", "message": "Input should be less than or equal to 100" }
  ]
}
Un format d’erreur standardisé permet aux applications clientes de gérer toutes les erreurs de la même manière. Elles peuvent analyser le champ code pour identifier le type de problème et utiliser message pour informer clairement l’utilisateur, sans avoir à développer un traitement spécifique pour chaque erreur.
