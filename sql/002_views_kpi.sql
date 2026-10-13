-- Vues KPI consommées par les nœuds Postgres du workflow n8n (specs/03-sql-kpis.md).
-- Référentiel temporel : date_veille = date la plus récente présente dans
-- raw_ventes (jamais CURRENT_DATE, pour que la démo reste correcte même
-- rejouée plusieurs jours après le chargement).

-- Bloc "CA de la veille"
CREATE OR REPLACE VIEW kpi_ca_veille AS
SELECT
    (SELECT max(dat_piece) FROM raw_ventes) AS date_veille,
    coalesce(sum(mt_ht), 0) AS ca
FROM raw_ventes
WHERE dat_piece = (SELECT max(dat_piece) FROM raw_ventes);

-- Bloc "Comparaison J-7"
CREATE OR REPLACE VIEW kpi_comparaison_j7 AS
WITH bornes AS (
    SELECT max(dat_piece) AS date_veille FROM raw_ventes
),
ca_veille AS (
    SELECT coalesce(sum(mt_ht), 0) AS ca
    FROM raw_ventes, bornes
    WHERE dat_piece = bornes.date_veille
),
ca_j7 AS (
    SELECT coalesce(sum(mt_ht), 0) AS ca
    FROM raw_ventes, bornes
    WHERE dat_piece = bornes.date_veille - 7
)
SELECT
    bornes.date_veille,
    ca_veille.ca AS ca_veille,
    ca_j7.ca AS ca_j7,
    ca_veille.ca - ca_j7.ca AS ecart_valeur,
    CASE WHEN ca_j7.ca = 0 THEN NULL
         ELSE round(100 * (ca_veille.ca - ca_j7.ca) / ca_j7.ca, 1)
    END AS ecart_pourcent
FROM bornes, ca_veille, ca_j7;

-- Bloc "Comparaison à la moyenne du mois" : moyenne journalière calculée sur
-- les jours calendaires écoulés depuis le 1er du mois jusqu'à date_veille
-- inclus (un jour sans vente compte donc comme 0, pas comme absent).
CREATE OR REPLACE VIEW kpi_comparaison_moyenne_mois AS
WITH mois AS (
    SELECT
        max(dat_piece) AS date_veille,
        date_trunc('month', max(dat_piece))::date AS debut_mois
    FROM raw_ventes
),
periode AS (
    SELECT
        mois.date_veille,
        mois.debut_mois,
        (mois.date_veille - mois.debut_mois + 1) AS jours_ecoules
    FROM mois
),
ca_veille AS (
    SELECT coalesce(sum(mt_ht), 0) AS ca
    FROM raw_ventes, periode
    WHERE dat_piece = periode.date_veille
),
ca_mois AS (
    SELECT coalesce(sum(mt_ht), 0) AS ca
    FROM raw_ventes, periode
    WHERE dat_piece BETWEEN periode.debut_mois AND periode.date_veille
)
SELECT
    periode.date_veille,
    ca_veille.ca AS ca_veille,
    round(ca_mois.ca / periode.jours_ecoules, 2) AS ca_moyen_mois,
    ca_veille.ca - round(ca_mois.ca / periode.jours_ecoules, 2) AS ecart_valeur,
    CASE WHEN ca_mois.ca = 0 THEN NULL
         ELSE round(
             100 * (ca_veille.ca - (ca_mois.ca / periode.jours_ecoules))
             / (ca_mois.ca / periode.jours_ecoules), 1
         )
    END AS ecart_pourcent
FROM periode, ca_veille, ca_mois;

-- Bloc "Top 5 clients" sur date_veille
CREATE OR REPLACE VIEW kpi_top_clients AS
SELECT
    cli_cod,
    cli_nom,
    sum(mt_ht) AS ca
FROM raw_ventes
WHERE dat_piece = (SELECT max(dat_piece) FROM raw_ventes)
GROUP BY cli_cod, cli_nom
ORDER BY ca DESC
LIMIT 5;

-- Bloc "Top 5 produits" sur date_veille
CREATE OR REPLACE VIEW kpi_top_produits AS
SELECT
    art_ref,
    art_lib,
    sum(mt_ht) AS ca
FROM raw_ventes
WHERE dat_piece = (SELECT max(dat_piece) FROM raw_ventes)
GROUP BY art_ref, art_lib
ORDER BY ca DESC
LIMIT 5;

-- Bloc "CA par région" sur date_veille
CREATE OR REPLACE VIEW kpi_ca_region AS
SELECT
    region,
    sum(mt_ht) AS ca
FROM raw_ventes
WHERE dat_piece = (SELECT max(dat_piece) FROM raw_ventes)
GROUP BY region
ORDER BY ca DESC;

-- Bloc "Alerte chute" : vrai si le CA de date_veille chute de plus de
-- SEUIL_ALERTE_CHUTE_PCT % par rapport à J-7. Seuil par défaut 15 %,
-- à ajuster ci-dessous si besoin.
CREATE OR REPLACE VIEW kpi_alerte_chute AS
SELECT
    date_veille,
    ca_veille,
    ca_j7,
    ecart_pourcent,
    (ca_j7 > 0 AND ecart_pourcent <= -15) AS alerte -- SEUIL_ALERTE_CHUTE_PCT = 15
FROM kpi_comparaison_j7;
