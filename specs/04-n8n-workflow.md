# 04 — Workflow n8n

**Statut :** Approved
**Dépend de :** [02-data-loader.md](02-data-loader.md), [03-sql-kpis.md](03-sql-kpis.md)

## Objectif

Orchestrer, chaque jour à 7h30, l'exécution du chargement, la lecture des KPI
et l'envoi du mail — avec une branche d'erreur explicite.

## Exigences fonctionnelles

- **Schedule Trigger** à 7h30 (cron n8n).
- Étape de chargement : exécution du loader (spec 02) sur le CSV du jour
  (nœud "Execute Command" ou équivalent). Le succès/échec de cette étape
  pilote la branche suivante.
- **Branche succès** : un nœud Postgres par vue KPI de la spec 03 (ou un seul
  nœud avec plusieurs requêtes), puis un nœud d'assemblage (Code ou HTML)
  qui construit le mail (spec 05), puis envoi (nœud Send Email / SMTP vers
  Mailpit).
- **Branche erreur** (fichier absent, vide, ou échec du loader — code de
  sortie non-zéro, cf. spec 02) : envoi d'un mail d'alerte simple
  ("Rapport non généré — [raison]"), **jamais** un rapport avec des chiffres
  faux ou à zéro.
- Pas de calcul de KPI en JavaScript dans un nœud Code : les agrégations
  restent des `SELECT` sur les vues SQL (cf. répartition des responsabilités,
  spec 00). Le nœud Code se limite à transformer le résultat des requêtes en
  HTML.
- Le workflow est exporté en JSON et versionné dans `n8n/`.

## Contrat d'interface

- Entrée : fichier CSV du jour dans `data/` (chemin fixe ou paramétrable via
  variable d'environnement n8n).
- Sortie : un mail reçu dans Mailpit, sujet du type
  `Rapport commercial — {date_veille}` (ou `ALERTE —` en cas d'erreur).

## Revue de répartition des responsabilités (à faire avant de clore cette spec)

- [ ] Vérifier qu'aucune agrégation métier n'a été réimplémentée dans un
  nœud Code n8n alors qu'elle existe déjà comme vue SQL.
- [ ] Vérifier qu'aucune logique de planification/envoi n'a été mise côté
  Python.

## Critères d'acceptation

- [ ] Le workflow se déclenche à l'heure planifiée (test manuel en
  déclenchant le trigger).
- [ ] Avec un CSV valide, le mail arrive dans Mailpit avec les 7 KPI de la
  spec 03.
- [ ] Avec un CSV généré en mode `--anomaly empty` ou `--anomaly
  missing-columns` (spec 01), le workflow envoie l'alerte et pas de rapport.
- [ ] Le JSON du workflow est présent dans `n8n/` et réimportable tel quel.
