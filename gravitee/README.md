# Configuration de Gravitee — procédure pas à pas

Console : http://localhost:8084 (admin / admin) · Portail : http://localhost:8085 · Gateway : http://localhost:8082

Les libellés correspondent à la Console APIM 4.x (Community Edition). Faire une capture d'écran à chaque étape marquée 📸 : elles servent au PowerPoint.

---

## A. Enregistrer l'API v1 et configurer son routage

1. **APIs** → **+ Add API** → tuile **Create New API** → **Import v4 API**.
2. **API format** : *OpenAPI specification* · **File source** : *Local file* · glisser `openapi/structures-v1.yaml`.
3. Cocher **Create documentation page from spec** (la doc apparaîtra sur le portail). Laisser la validation OpenAPI décochée.
4. **Import**. L'API est créée en état **CREATED**, privée, non démarrée. 📸
5. **Configuration → Entrypoints** : remplacer le context path proposé (`/api/v1`) par **`/sante/structures/v1`** → Save.
6. **Endpoints** : vérifier que la cible est `http://structures-api:8000/api/v1` (sinon la corriger). 📸
7. **Consumers → Plans → + Add new plan → Keyless** nommé `Découverte` → Create, puis publier le plan (icône nuage).
8. Bandeau en haut : **Deploy API**, puis **Configuration → General → Danger Zone → Start the API**.
9. Test : `curl http://localhost:8082/sante/structures/v1/structures` → 200 et la liste paginée. 📸

## B. Plan sécurisé avec quota

1. **Consumers → Plans → + Add new plan → API Key**.
2. Étape *General* : nom `Standard`, description « Accès authentifié, 5 req / 10 s, 1 000 req / jour », **Auto validate subscription : OFF** (validation manuelle).
3. Étape *Restriction* :
   - **Rate limiting** : 5 requêtes par 10 secondes.
   - **Quota** : 1 000 requêtes par jour.
4. **Create**, puis publier le plan Standard (icône nuage). 📸
5. Fermer le plan `Découverte` (icône de fermeture) pour que l'accès sans clé ne soit plus possible.
6. **Deploy API** (bandeau en haut).
7. Test : `curl -i http://localhost:8082/sante/structures/v1/structures` → **401**.

## C. Application consommatrice et souscription

1. Menu principal **Applications → + Add Application** : nom `App Ministère Santé`, description « Tableau de bord régional (fictif) », type *Simple*. 📸
2. Dans l'application : **Subscriptions → + Create a subscription** → choisir l'API *Structures sanitaires 1.0.0* et le plan **Standard**.
   - Variante plus parlante pour la démo : se connecter au **portail** (http://localhost:8085), ouvrir l'API, cliquer **Subscribe**, choisir le plan Standard et l'application.
3. La souscription est **PENDING**. Côté API : **Consumers → Subscriptions** → ouvrir la souscription → **Validate**. 📸
4. Dans le détail de la souscription, copier la **clé d'API** et la coller dans la variable `api_key` de l'environnement Postman.
5. Tests :
   ```
   curl -i http://localhost:8082/sante/structures/v1/structures/1 -H "X-Gravitee-Api-Key: <clé>"   # 200
   ./scripts/test-quota.sh <clé>                                                                    # 429 dès le 6e appel
   ```
6. Droits d'accès : créer une 2e application `App Test Sans Droit` **sans souscription** → elle n'a aucune clé valide → 401. Optionnel : **Close** sur une souscription puis rappel avec sa clé → 401. 📸

## D. Cycle de vie (création → publication → retrait → nouvelle version)

| Action dans la Console | Où | État cycle de vie | État d'exécution | Visible portail | Appel gateway |
|---|---|---|---|---|---|
| Import (fait en A) | — | CREATED | STOPPED puis STARTED | Non | 200 |
| **Publish the API** | Configuration → General → Danger Zone | PUBLISHED | STARTED | Oui | 200 |
| **Unpublish the API** (retrait temporaire) | idem | UNPUBLISHED | STARTED | Non | **200** pour les abonnés |
| **Stop the API** (arrêt technique) | idem | inchangé | STOPPED | inchangé | **refusé** (404) |
| Start + Publish | idem | PUBLISHED | STARTED | Oui | 200 |

1. **Publier** : *Publish the API*. Rendre l'API visible : *Make public* dans la même zone si elle n'apparaît pas sur le portail. Vérifier sur http://localhost:8085 que l'API et sa documentation apparaissent. 📸
2. **Retrait temporaire** : *Unpublish the API* → l'API disparaît du portail, mais la requête Postman du dossier 4 « Après UNPUBLISH » répond **200**. 📸 + 📸
3. **Arrêt technique** : *Stop the API* → la requête « Après STOP » n'est plus routée (404). L'API reste visible dans la Console. 📸
4. Remettre en service : *Start the API* puis *Publish the API*.

**Conclusion à présenter** : le retrait de publication agit sur la *visibilité* et les *nouvelles souscriptions* ; l'arrêt technique agit sur le *trafic*. Ce sont deux états indépendants dans Gravitee.

### Nouvelle version (v2)

1. Importer `openapi/structures-v2.yaml` (même procédure qu'en A), context path **`/sante/structures/v2`**, endpoint `http://structures-api:8000/api/v2`.
2. Créer un plan API Key `Standard v2` (mêmes restrictions), le publier, déployer, démarrer, publier l'API.
3. Faire souscrire `App Ministère Santé` au plan v2, valider, copier la clé dans `api_key_v2` (Postman).
4. Sur l'API v1 : **Deprecate** le plan `Standard` → plus de nouvelle souscription à la v1, les abonnés existants continuent de fonctionner pendant la migration. 📸
5. Uniquement à la toute fin (irréversible) : *Deprecate* sur l'API v1 elle-même.

## E. Export pour la reproductibilité

Pour chaque API : **Configuration → General → Export** (format JSON) → enregistrer sous `gravitee/api-structures-v1.json` et `gravitee/api-structures-v2.json`, puis commit.

Réimport sur une machine neuve : **APIs → + Add API → Import v4 API → API format : Gravitee definition** → choisir le fichier. Les applications, souscriptions et clés ne font pas partie de l'export : refaire la partie C.
