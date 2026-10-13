# 02 — Chargement Postgres

**Statut :** Approved
**Dépend de :** [01-data-generator.md](01-data-generator.md)

## Objectif

Lire le CSV "export ERP", le nettoyer légèrement et le charger dans Postgres,
de façon idempotente : rejouer le script sur le même fichier ne doit jamais
créer de doublons.

## Exigences fonctionnelles

- Script Python (`loader/`), pas de dépendance à n8n.
- Entrée : chemin d'un CSV conforme au contrat de la spec 01.
- Nettoyage attendu (léger, pas de logique métier/agrégation ici) :
  - typage des colonnes (`QTE` → entier, `MT_HT` → décimal, `DAT_PIECE` → date).
  - conversion virgule → point décimal.
  - conversion date `JJ/MM/AAAA` → type date SQL.
- Chargement dans une table unique `raw_ventes` (schéma ci-dessous).
- **Idempotence** : stratégie à base de clé unique (`num_piece`) + upsert
  (`INSERT ... ON CONFLICT DO UPDATE`), ou suppression des lignes de la date
  concernée avant réinsertion. Le choix doit être documenté en commentaire
  dans le script.

## Gestion d'erreur (fichier absent / vide / colonnes manquantes)

- Le script doit **échouer avec un code de sortie non-zéro et un message
  clair** si :
  - le fichier n'existe pas,
  - le fichier est vide (0 ligne de données),
  - une colonne obligatoire du contrat (spec 01) est absente.
- Le script ne doit **jamais** charger de données partielles/invalides en
  base. C'est ce signal d'échec que n8n utilisera pour déclencher l'alerte
  (spec 04) — la logique de détection d'anomalie vit ici, pas en SQL ni en n8n.

## Contrat de sortie — schéma `raw_ventes`

| Colonne | Type SQL | Contrainte |
|---|---|---|
| `num_piece` | text | UNIQUE, NOT NULL |
| `dat_piece` | date | NOT NULL |
| `cli_cod` | text | NOT NULL |
| `cli_nom` | text | |
| `art_ref` | text | NOT NULL |
| `art_lib` | text | |
| `region` | text | NOT NULL |
| `qte` | integer | |
| `mt_ht` | numeric(12,2) | |
| `loaded_at` | timestamptz | défaut `now()` |

## Interface CLI (indicative)

```
python loader/load.py --file data/export_2026-10-12.csv
```

Code de sortie `0` = succès, `!= 0` = échec (déclenche l'alerte n8n).

## Critères d'acceptation

- [ ] Charger un CSV valide crée les lignes attendues dans `raw_ventes`.
- [ ] Recharger le **même** fichier une deuxième fois ne crée aucun doublon
  (vérifié par un `COUNT(*)` avant/après).
- [ ] Charger un fichier vide retourne un code de sortie non-zéro, sans
  toucher à la base.
- [ ] Charger un fichier avec une colonne manquante retourne un code de
  sortie non-zéro, sans toucher à la base.
