"""Génère des CSV fictifs imitant un export d'ERP (voir specs/01-data-generator.md)."""

import argparse
import csv
import random
import sys
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

SEED = 42
N_CLIENTS = 25
MIN_LINES_PER_DAY = 20
MAX_LINES_PER_DAY = 80

COLUMNS = [
    "NUM_PIECE", "DAT_PIECE", "CLI_COD", "CLI_NOM",
    "ART_REF", "ART_LIB", "REGION", "QTE", "MT_HT",
]

REGIONS = [
    "Ile-de-France",
    "Auvergne-Rhone-Alpes",
    "Nouvelle-Aquitaine",
    "Occitanie",
    "Hauts-de-France",
    "Grand Est",
]

# Catalogue fixe : un distributeur de gros ne renouvelle pas son catalogue
# tous les jours, et il faut des clients/produits récurrents pour que les
# "top 5" aient un sens sur plusieurs mois.
PRODUCT_NAMES = [
    "Carton de gants nitrile", "Palette de bouteilles PET 1L",
    "Rouleau de film etirable", "Lot de cartons d'emballage 40x30",
    "Palette de briques de lait UHT", "Carton de bouteilles d'eau 50cl",
    "Lot de sacs kraft", "Carton de gobelets jetables",
    "Rouleau de papier essuyage industriel", "Palette de conserves 1/2",
    "Carton de sacs poubelle 100L", "Lot de gants de protection cuir",
    "Palette de briques de jus de fruit", "Carton de serviettes en papier",
    "Lot de palettes bois EUR", "Carton de bouteilles d'huile 1L",
    "Rouleau de ruban adhesif emballage", "Palette de packs d'eau gazeuse",
    "Carton de boites de conserve legumes", "Lot de housses plastique palette",
    "Carton de bidons de detergent 5L", "Palette de sacs de farine 25kg",
    "Carton de boites de cafe moulu", "Lot de caisses plastique gerbables",
    "Palette de packs de biere 33cl",
]


def build_reference_data() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    fake = Faker("fr_FR")
    fake.seed_instance(SEED)
    clients = [(f"CLI-{i:04d}", fake.company()) for i in range(1, N_CLIENTS + 1)]
    products = [(f"ART-{i:04d}", name) for i, name in enumerate(PRODUCT_NAMES, start=1)]
    return clients, products


def format_amount(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def format_date(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def generate_day_rows(
    day: date,
    clients: list[tuple[str, str]],
    products: list[tuple[str, str]],
    rng: random.Random,
) -> list[list[str]]:
    n_lines = rng.randint(MIN_LINES_PER_DAY, MAX_LINES_PER_DAY)
    rows = []
    for i in range(1, n_lines + 1):
        cli_cod, cli_nom = rng.choice(clients)
        art_ref, art_lib = rng.choice(products)
        region = rng.choice(REGIONS)
        qte = rng.randint(1, 50)
        mt_ht = round(rng.uniform(20, 3000), 2)
        num_piece = f"VT-{day.strftime('%Y%m%d')}-{i:04d}"
        rows.append([
            num_piece, format_date(day), cli_cod, cli_nom,
            art_ref, art_lib, region, str(qte), format_amount(mt_ht),
        ])
    return rows


def rows_for_day(day: date, clients, products) -> list[list[str]]:
    # seed dérivé de la date : la même journée régénère toujours les mêmes lignes.
    rng = random.Random(SEED + day.toordinal())
    return generate_day_rows(day, clients, products, rng)


def write_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(COLUMNS)
        writer.writerows(rows)


def write_anomaly(path: Path, kind: str, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if kind == "empty":
        path.write_bytes(b"")
        return
    if kind == "missing-columns":
        dropped_index = COLUMNS.index("REGION")
        broken_columns = [c for c in COLUMNS if c != "REGION"]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(broken_columns)
            for row in rows:
                writer.writerow([v for j, v in enumerate(row) if j != dropped_index])
        return
    raise ValueError(f"Type d'anomalie inconnu : {kind}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="Jour a generer, format AAAA-MM-JJ")
    parser.add_argument("--out", help="Chemin du CSV de sortie (avec --date)")
    parser.add_argument(
        "--historique",
        help="Plage a generer, format AAAA-MM-JJ:AAAA-MM-JJ (un fichier par jour)",
    )
    parser.add_argument("--out-dir", default="data", help="Dossier de sortie (avec --historique)")
    parser.add_argument(
        "--anomaly",
        choices=["empty", "missing-columns"],
        help="Genere un CSV casse au lieu d'un export valide (avec --date)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    clients, products = build_reference_data()

    if args.historique:
        start_str, end_str = args.historique.split(":")
        start, end = date.fromisoformat(start_str), date.fromisoformat(end_str)
        out_dir = Path(args.out_dir)
        day = start
        count = 0
        while day <= end:
            rows = rows_for_day(day, clients, products)
            write_csv(out_dir / f"export_{day.isoformat()}.csv", rows)
            day += timedelta(days=1)
            count += 1
        print(f"{count} fichiers generes dans {out_dir} ({start} -> {end})")
        return

    if args.date:
        day = date.fromisoformat(args.date)
        out_path = Path(args.out) if args.out else Path("data") / f"export_{day.isoformat()}.csv"
        rows = rows_for_day(day, clients, products)
        if args.anomaly:
            write_anomaly(out_path, args.anomaly, rows)
        else:
            write_csv(out_path, rows)
        print(f"Fichier genere : {out_path}")
        return

    print("Specifier --date ou --historique (voir --help)", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
