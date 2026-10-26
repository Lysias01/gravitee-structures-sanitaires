-- =====================================================================
-- Projet : Gestion du cycle de vie des API avec Gravitee (Thème 22)
-- Groupe : SI Groupe 2 — IBAM 2026
-- Fichier : 01_schema.sql — création du schéma de la base de référence
-- Exécuté automatiquement par PostgreSQL au premier démarrage du conteneur
-- (dossier /docker-entrypoint-initdb.d).
-- =====================================================================

CREATE TABLE IF NOT EXISTS structures_sanitaires (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(20)  NOT NULL UNIQUE,
    nom             VARCHAR(150) NOT NULL,
    type            VARCHAR(20)  NOT NULL
                    CHECK (type IN ('CHU', 'CHR', 'CMA', 'CSPS', 'CLINIQUE')),
    statut          VARCHAR(10)  NOT NULL
                    CHECK (statut IN ('PUBLIC', 'PRIVE')),
    region          VARCHAR(60)  NOT NULL,
    ville           VARCHAR(80)  NOT NULL,
    nombre_lits     INTEGER      NOT NULL DEFAULT 0 CHECK (nombre_lits >= 0),
    telephone       VARCHAR(20),
    services        TEXT[]       NOT NULL DEFAULT '{}',
    date_ouverture  DATE,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now()
);

COMMENT ON TABLE  structures_sanitaires IS 'Référentiel fictif des structures sanitaires (données de démonstration)';
COMMENT ON COLUMN structures_sanitaires.code   IS 'Identifiant métier unique, format TYPE-REG-NNN';
COMMENT ON COLUMN structures_sanitaires.type   IS 'CHU, CHR, CMA, CSPS ou CLINIQUE';
COMMENT ON COLUMN structures_sanitaires.statut IS 'PUBLIC ou PRIVE';

CREATE INDEX IF NOT EXISTS idx_structures_region ON structures_sanitaires (lower(region));
CREATE INDEX IF NOT EXISTS idx_structures_ville  ON structures_sanitaires (lower(ville));
CREATE INDEX IF NOT EXISTS idx_structures_type   ON structures_sanitaires (type);
CREATE INDEX IF NOT EXISTS idx_structures_nom    ON structures_sanitaires (lower(nom));
