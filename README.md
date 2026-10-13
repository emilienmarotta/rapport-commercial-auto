# Rapport commercial automatique

> Projet de démonstration (portfolio Malt, profil data engineer).
> **Données 100 % fictives.**

## Le problème

Dans une PME fictive de commerce de gros, le directeur commercial perd chaque
matin 20 à 30 minutes à ouvrir l'ERP, exporter un fichier et le mettre en
forme pour avoir une vision de l'activité de la veille.

## La solution

Chaque matin à 7h30, il reçoit un mail automatique avec les chiffres de la
veille (CA, comparaisons, top clients, top produits, CA par région, alerte en
cas de chute), sans aucune intervention humaine.

![Schéma du flux : Python génère et charge les données dans PostgreSQL, n8n planifie, lit les KPI et envoie le mail](docs/schema-flux.png)

```
Générateur de données → CSV « export ERP » → Python (nettoyage + chargement)
→ PostgreSQL → n8n (planification + requêtes SQL + mise en forme) → Mail
```

**Temps gagné (hypothèse de scénario, pas une mesure réelle)** : si ce mail
remplace effectivement les 20 minutes d'export/mise en forme manuelle
évoquées plus haut, cela représente environ 20 min × 220 jours ouvrés ≈ 73 h
par an. C'est un ordre de grandeur pour ce scénario fictif, pas un résultat
mesuré sur une vraie PME.

## Ce que ça démontre techniquement

- **Python** génère les données fictives, nettoie et charge dans PostgreSQL
  de façon idempotente. Aucune logique d'orchestration ni de mise en forme
  du mail côté Python.
- **n8n** orchestre tout le reste : déclenchement planifié, lecture des KPI
  via des vues SQL, assemblage et envoi du mail, gestion de la branche
  d'erreur. Les agrégations métier (CA, comparaisons, tops, alerte) restent
  des `SELECT` sur des vues SQL visibles dans les nœuds Postgres du
  workflow — jamais recalculées en JavaScript.
- **Mailpit** capte les mails en local (pas d'envoi réel).
- Approche *specs-driven* : chaque brique est spécifiée dans
  [`specs/`](specs/) et validée avant d'être codée. Avancement par
  milestone : [`ROADMAP.md`](ROADMAP.md) ; statut détaillé de chaque spec :
  [`specs/README.md`](specs/README.md).

## Capture du mail reçu

![Capture du mail de rapport commercial affiché dans l'interface web de Mailpit](docs/capture-mail.png)

## Comment relancer la démo

```bash
cp .env.example .env
docker compose up -d
```

- n8n : http://localhost:5678
- Mailpit (boîte mail locale) : http://localhost:8025
- Postgres : localhost:5432 (identifiants dans `.env`)

Le compte n8n et les identifiants des nœuds (Postgres, SMTP) vivent dans le
volume Docker `n8n_data`, donc pas versionnés avec le code. Au premier
démarrage :

1. Créer un compte propriétaire dans l'UI n8n (http://localhost:5678).
2. Importer le workflow : `docker compose exec n8n n8n import:workflow
   --input=/workflows/rapport-commercial-quotidien.json`.
   (si la CLI demande un `--userId`, le récupérer dans l'UI n8n —
   Paramètres → Utilisateurs.)
3. Dans l'UI n8n, créer les identifiants Postgres (host `postgres`, base/
   utilisateur/mot de passe de `.env`) et SMTP (host `mailpit`, port `1025`,
   sans authentification) et les associer aux nœuds correspondants du
   workflow.
4. Activer le workflow, ou le déclencher manuellement pour tester.

## Structure du dépôt

```
rapport-commercial-auto/
├── docker-compose.yml
├── .env.example
├── specs/                 # spécifications (lues avant d'écrire du code)
├── data/                  # CSV générés (ignorés par git, sauf échantillon)
├── generator/             # génération des données fictives
├── loader/                # nettoyage + chargement Postgres + API HTTP interne
├── sql/                   # schéma, vues et requêtes KPI
├── n8n/                   # workflow exporté en JSON
└── docs/                  # schéma du flux, capture du mail
```

## Limites assumées

- Données entièrement fictives, aucun lien avec un vrai ERP.
- Démo locale uniquement (pas d'hébergement).
- Pas d'authentification multi-utilisateurs ni de volumétrie réaliste : ce
  projet démontre un mécanisme, pas un produit prêt pour la production.
