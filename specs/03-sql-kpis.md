# 03 — Vues et requêtes KPI

**Statut :** Approved
**Dépend de :** [02-data-loader.md](02-data-loader.md)

## Objectif

Fournir, pour chaque bloc du mail, une vue ou requête SQL propre et lisible,
exécutable directement par un nœud Postgres de n8n (pas de logique métier
cachée en Python).

## Exigences fonctionnelles

Fichiers SQL dans `sql/`, un fichier par thème au minimum (`schema.sql`,
`views_kpi.sql`). Toutes les requêtes prennent comme référentiel temporel
**la date la plus récente présente dans `raw_ventes`** (pas `CURRENT_DATE`,
pour que la démo reste cohérente même rejouée plusieurs jours plus tard) —
appelée ci-dessous `date_veille`.

## KPI à livrer

1. **CA de la veille** — somme de `mt_ht` pour `dat_piece = date_veille`.
2. **Comparaison J-7** — CA de `date_veille` vs CA de `date_veille - 7 jours`,
  en valeur et en %.
3. **Comparaison moyenne du mois** — CA de `date_veille` vs moyenne
  journalière du CA sur le mois en cours (jours écoulés jusqu'à
  `date_veille`).
4. **Top 5 clients** — par somme de `mt_ht`, sur `date_veille` (ou sur une
  fenêtre glissante à définir — par défaut : la journée `date_veille`).
5. **Top 5 produits** — idem, par `art_ref`/`art_lib`.
6. **CA par région** — somme de `mt_ht` groupée par `region`, sur
  `date_veille`.
7. **Détection de chute** — booléen/flag si le CA de `date_veille` chute de
  plus de `X %` par rapport à J-7 (seuil `X` paramétrable, valeur par défaut
  **15 %**, passée en paramètre de requête ou en constante documentée en
  tête du fichier SQL).

## Contrat d'interface

Chaque KPI est exposé comme une **vue** (`CREATE VIEW kpi_xxx AS ...`) afin
qu'un nœud Postgres n8n puisse faire un simple `SELECT * FROM kpi_xxx`.
Noms de vues :

- `kpi_ca_veille`
- `kpi_comparaison_j7`
- `kpi_comparaison_moyenne_mois`
- `kpi_top_clients`
- `kpi_top_produits`
- `kpi_ca_region`
- `kpi_alerte_chute`

## Critères d'acceptation

- [ ] Chaque vue s'exécute seule (`SELECT * FROM kpi_xxx;`) sans erreur sur
  les données générées par la spec 01.
- [ ] `kpi_alerte_chute` renvoie bien un flag "vrai" quand on injecte
  artificiellement une journée à CA très bas (test manuel).
- [ ] Les vues restent correctes si on les rejoue un autre jour (pas de
  dépendance à `CURRENT_DATE`).
- [ ] SQL commenté : chaque vue indique en tête à quel bloc du mail elle
  correspond.
