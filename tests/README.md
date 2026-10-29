# Tests du projet

Ce dossier contient la collection Postman du projet (`postman/`) et les résultats d'exécution obtenus avec Newman (`resultats/`).

### Les 4 dossiers de la collection Postman

| Dossier | Ce qu'il vérifie |
|---|---|
| 1. Backend direct | L'API appelée sans passer par la gateway : santé du service, liste paginée, recherche, détail d'une structure, erreurs 400 / 404 / 405 et nouveau format de la version 2. |
| 2. Gateway Gravitee - accès et quota | La sécurité de la gateway : refus (401) sans clé ou avec une clé inventée, scénario de bout en bout avec une clé valide, erreur du backend relayée par la gateway, et blocage (429) quand on dépasse 5 requêtes en 10 secondes. |
| 3. Gateway Gravitee - version 2 | L'accès à la version 2 de l'API à travers la gateway, avec sa propre souscription. |
| 4. Cycle de vie (manuel) | Le comportement de l'API selon son état dans Gravitee : elle répond toujours (200) après un retrait de publication, mais la gateway ne la route plus après un arrêt. Ces tests se lancent à la main, après avoir changé l'état de l'API dans la console. |

### Résultat obtenu avec Newman

L'exécution complète de la collection a donné :

- **26 requêtes** envoyées ;
- **44 vérifications** (assertions) ;
- **0 échec**.

Le rapport détaillé se trouve dans `resultats/newman-complet.json`.

### Ce que prouve le test de bout en bout

Le test « Bout en bout - Clé valide » utilise la clé d'API obtenue en souscrivant au plan dans Gravitee. Il montre que toute la chaîne fonctionne :

```
clé de souscription → gateway Gravitee → API → base de données
```

La gateway accepte la clé et transmet la requête à l'API, qui interroge la base. La réponse contient exactement la structure `CHU-CEN-001` (CHU Fictif de Ouagadougou Nord) insérée par le script `db/init/02_seed.sql`. On est donc sûr que les données viennent bien de la base, et pas d'une réponse simulée.
