"""Charge un CSV "export ERP" dans Postgres, de façon idempotente (specs/02-data-loader.md)."""

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

import psycopg
from dotenv import load_dotenv

REQUIRED_COLUMNS = [
    "NUM_PIECE", "DAT_PIECE", "CLI_COD", "CLI_NOM",
    "ART_REF", "ART_LIB", "REGION", "QTE", "MT_HT",
]

# Idempotence : upsert sur num_piece (clé unique), pas de suppression/réinsertion
# par date — ça permet de rejouer un fichier plusieurs fois sans jamais créer
# de doublon ni perdre une ligne corrigée entre deux générations.
UPSERT_SQL = """
INSERT INTO raw_ventes (
    num_piece, dat_piece, cli_cod, cli_nom, art_ref, art_lib, region, qte, mt_ht
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (num_piece) DO UPDATE SET
    dat_piece = EXCLUDED.dat_piece,
    cli_cod = EXCLUDED.cli_cod,
    cli_nom = EXCLUDED.cli_nom,
    art_ref = EXCLUDED.art_ref,
    art_lib = EXCLUDED.art_lib,
    region = EXCLUDED.region,
    qte = EXCLUDED.qte,
    mt_ht = EXCLUDED.mt_ht
"""


class LoadError(Exception):
    """Fichier invalide : rien ne doit être écrit en base."""


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise LoadError(f"fichier introuvable : {path}")
    if path.stat().st_size == 0:
        raise LoadError(f"fichier vide : {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
        if missing:
            raise LoadError(f"colonne(s) manquante(s) : {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise LoadError(f"fichier vide (0 ligne de données) : {path}")
    return rows


def parse_row(row: dict[str, str]) -> tuple:
    try:
        dat_piece = datetime.strptime(row["DAT_PIECE"], "%d/%m/%Y").date()
        qte = int(row["QTE"]) if row["QTE"] else None
        mt_ht = float(row["MT_HT"].replace(",", ".")) if row["MT_HT"] else None
    except ValueError as exc:
        raise LoadError(f"ligne invalide ({row.get('NUM_PIECE', '?')}) : {exc}") from exc
    return (
        row["NUM_PIECE"], dat_piece, row["CLI_COD"], row["CLI_NOM"],
        row["ART_REF"], row["ART_LIB"], row["REGION"], qte, mt_ht,
    )


def load_file(path: Path) -> int:
    rows = read_rows(path)
    values = [parse_row(row) for row in rows]

    load_dotenv()
    conn = psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", "5432"),
        dbname=os.environ.get("POSTGRES_DB", "rapport_commercial"),
        user=os.environ.get("POSTGRES_USER", "rapport_user"),
        password=os.environ.get("POSTGRES_PASSWORD", "change_me"),
    )
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(UPSERT_SQL, values)
    finally:
        conn.close()
    return len(values)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, help="Chemin du CSV a charger")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        count = load_file(Path(args.file))
    except LoadError as exc:
        print(f"Erreur de chargement : {exc}", file=sys.stderr)
        sys.exit(1)
    except psycopg.Error as exc:
        print(f"Erreur base de donnees : {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"{count} lignes chargees dans raw_ventes depuis {args.file}")


if __name__ == "__main__":
    main()
