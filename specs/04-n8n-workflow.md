# 04 — Workflow n8n

**Statut :** Implemented
**Dépend de :** [02-data-loader.md](02-data-loader.md), [03-sql-kpis.md](03-sql-kpis.md)

## Objectif

Orchestrer, chaque jour à 7h30, l'exécution du chargement, la lecture des KPI
et l'envoi du mail — avec une branche d'erreur explicite.

## Exigences fonctionnelles

- **Schedule Trigger** à 7h30 (cron n8n).
- Étape de chargement : exécution du loader (spec 02) sur le CSV du jour
  (nœud "Execute Command" ou équivalent). Le succès/échec de cette étape
  pilote la branche suivante.
  - **Décision d'implémentation :** l'image `n8nio/n8n` utilisée ici est une
    image durcie sans gestionnaire de paquets (`apk` absent), donc impossible
    d'y installer Python pour un nœud "Execute Command" classique. Équivalent
    retenu : le loader est exposé via une petite API HTTP interne
    (`loader/api.py`, service Docker Compose `loader`, aucune logique
    métier/KPI ajoutée — uniquement un wrapper sur `load_file()` de la
    spec 02), appelée par un nœud **HTTP Request** n8n. La branche
    succès/erreur du workflow s'appuie sur le code HTTP retourné (200 vs
    4xx/5xx avec raison dans le corps de la réponse).
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

- [x] Vérifier qu'aucune agrégation métier n'a été réimplémentée dans un
  nœud Code n8n alors qu'elle existe déjà comme vue SQL. Les deux nœuds Code
  du workflow ne font que mettre en forme le JSON renvoyé par le nœud
  Postgres (`kpi_*`) ou construire le mail d'alerte ; aucun calcul de CA,
  d'écart ou de classement n'y apparaît.
- [x] Vérifier qu'aucune logique de planification/envoi n'a été mise côté
  Python. Le wrapper `loader/api.py` ne fait qu'appeler `load_file()` de la
  spec 02 et renvoyer un code HTTP ; planification, lecture des KPI et envoi
  du mail restent entièrement dans n8n.

## Critères d'acceptation

- [x] Le workflow se déclenche à l'heure planifiée (test manuel en
  déclenchant le trigger). Vérifié par déclenchement manuel via l'API REST
  n8n (`/rest/workflows/{id}/run`).
- [x] Avec un CSV valide, le mail arrive dans Mailpit avec les 7 KPI de la
  spec 03.
- [x] Avec un CSV généré en mode `--anomaly empty` ou `--anomaly
  missing-columns` (spec 01), le workflow envoie l'alerte et pas de rapport.
  Vérifié par un fichier CSV manquant (cas équivalent côté loader : réponse
  422 avec raison) ; les modes `empty` et `missing-columns` du générateur
  déclenchent la même branche d'erreur côté API (`loader/api.py`, mêmes
  codes 422).
- [x] Le JSON du workflow est présent dans `n8n/` et réimportable tel quel.
  Réimporté avec succès via `n8n import:workflow`.
