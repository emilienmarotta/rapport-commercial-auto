# 01 — Générateur de données fictives

**Statut :** Approved
**Dépend de :** [00-vision.md](00-vision.md)

## Objectif

Produire un CSV qui imite un vrai export d'ERP mal fichu, plus un historique
exploitable pour les comparaisons (J-7, moyenne du mois), et permettre
d'injecter des anomalies pour tester la branche d'erreur.

## Exigences fonctionnelles

- Script Python (`generator/`), utilise `Faker`.
- Génère les ventes d'**une journée** par exécution (le CSV "du jour").
- Doit aussi pouvoir générer un **historique** de 2 à 3 mois en une seule
  commande (un fichier par jour, ou un fichier unique avec toutes les lignes
  — à trancher à l'implémentation, mais le format de sortie doit être
  identique à un export "du jour").
- Mode `--anomaly {empty,missing-columns}` : produit un CSV cassé
  volontairement, pour tester la branche d'erreur du workflow n8n (spec 04).

## Contrat de sortie — format CSV

- Séparateur `;`.
- Dates au format `JJ/MM/AAAA`.
- Décimales avec virgule (`1234,56`).
- Encodage et noms de colonnes volontairement peu parlants :

| Colonne | Signification réelle | Type |
|---|---|---|
| `NUM_PIECE` | Identifiant de la vente (unique) | string |
| `DAT_PIECE` | Date de la vente | date `JJ/MM/AAAA` |
| `CLI_COD` | Code client | string |
| `CLI_NOM` | Nom du client | string |
| `ART_REF` | Référence produit | string |
| `ART_LIB` | Libellé produit | string |
| `REGION` | Région de vente | string |
| `QTE` | Quantité vendue | entier |
| `MT_HT` | Montant HT | décimal, virgule |

- `NUM_PIECE` doit être unique sur l'ensemble de l'historique généré (c'est la
  clé qui permettra l'upsert idempotent côté loader, spec 02).
- Volumétrie : de l'ordre de 20 à 80 lignes par jour (assez pour des top 5
  crédibles, assez peu pour rester lisible).
- Doit couvrir au moins 5 régions et une vingtaine de clients/produits
  distincts pour que les agrégations (top 5, par région) aient du sens.

## Interface CLI (indicative)

```
python generator/generate.py --date 2026-10-12 --out data/export_2026-10-12.csv
python generator/generate.py --historique 2026-07-01:2026-10-12 --out-dir data/
python generator/generate.py --date 2026-10-12 --anomaly empty --out data/export_broken.csv
```

## Critères d'acceptation

- [ ] Un CSV généré s'ouvre proprement avec séparateur `;` et virgule décimale.
- [ ] Les noms de colonnes correspondent exactement au tableau ci-dessus.
- [ ] `NUM_PIECE` est unique sur tout l'historique généré.
- [ ] L'historique couvre 2 à 3 mois sans trou de date.
- [ ] Le mode `--anomaly empty` produit un fichier vide (0 ligne de données).
- [ ] Le mode `--anomaly missing-columns` produit un CSV avec au moins une
  colonne manquante par rapport au contrat.
