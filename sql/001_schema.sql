-- Schéma de base : table brute alimentée par le loader (specs/02-data-loader.md).
-- Monté dans /docker-entrypoint-initdb.d : exécuté automatiquement à la
-- création du volume Postgres (premier `docker compose up`).

CREATE TABLE IF NOT EXISTS raw_ventes (
    num_piece  text PRIMARY KEY,
    dat_piece  date NOT NULL,
    cli_cod    text NOT NULL,
    cli_nom    text,
    art_ref    text NOT NULL,
    art_lib    text,
    region     text NOT NULL,
    qte        integer,
    mt_ht      numeric(12, 2),
    loaded_at  timestamptz NOT NULL DEFAULT now()
);
