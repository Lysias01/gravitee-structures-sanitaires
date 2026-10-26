# Envoie 8 appels rapides à la gateway pour démontrer la limite 5 req / 10 s (429).
# Usage : .\scripts\test-quota.ps1 -Key <cle_api>
param(
    [Parameter(Mandatory = $true)][string]$Key,
    [string]$Url = "http://localhost:8082/sante/structures/v1/structures"
)
for ($i = 1; $i -le 8; $i++) {
    try {
        $r = Invoke-WebRequest -Uri $Url -Headers @{ "X-Gravitee-Api-Key" = $Key } -UseBasicParsing
        Write-Output "Appel $i -> HTTP $($r.StatusCode)"
    } catch {
        Write-Output "Appel $i -> HTTP $($_.Exception.Response.StatusCode.value__)"
    }
}
