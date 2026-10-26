#!/usr/bin/env bash
# Envoie 8 appels rapides à la gateway pour démontrer la limite 5 req / 10 s (429).
# Usage : ./scripts/test-quota.sh <cle_api> [url]
KEY="${1:?Usage: $0 <cle_api> [url]}"
URL="${2:-http://localhost:8082/sante/structures/v1/structures}"
for i in $(seq 1 8); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -H "X-Gravitee-Api-Key: $KEY" "$URL")
  echo "Appel $i -> HTTP $code"
done
