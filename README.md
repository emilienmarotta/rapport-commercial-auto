# Rapport commercial automatique

> Projet de démonstration (portfolio Malt). **Données 100 % fictives.**
> Le temps gagné indiqué est une hypothèse de scénario, pas une mesure réelle.

## Le problème

Dans une PME fictive de commerce de gros, le directeur commercial perd chaque
matin 20 à 30 minutes à ouvrir l'ERP, exporter un fichier et le mettre en
forme pour avoir une vision de l'activité de la veille.

## La solution

Chaque matin à 7h30, il reçoit un mail avec les chiffres de la veille
(CA, comparaisons, top clients, top produits, CA par région, alerte en cas de
chute), sans aucune intervention humaine.

## Architecture

```
Générateur de données → CSV « export ERP » → Python (nettoyage + chargement)
→ PostgreSQL → n8n (planification + requêtes SQL + mise en forme) → Mail
```

- **Python** génère les données fictives, nettoie et charge dans Postgres.
- **n8n** orchestre : déclenchement planifié, requêtes SQL sur les KPI,
  assemblage et envoi du mail, gestion de la branche d'erreur.
- **Mailpit** capte les mails en local (pas d'envoi réel).

Détail complet des choix et des contrats entre composants : voir [`specs/`](specs/).

## Statut du projet

Projet construit en suivant une approche *specs-driven* : chaque brique est
spécifiée dans [`specs/`](specs/) avant d'être codée. Avancement par
milestone : [`ROADMAP.md`](ROADMAP.md). État détaillé de chaque spec :
[`specs/README.md`](specs/README.md).

## Lancer la démo

```bash
cp .env.example .env
docker compose up -d
```

- n8n : http://localhost:5678
- Mailpit (boîte mail locale) : http://localhost:8025
- Postgres : localhost:5432 (identifiants dans `.env`)

## Structure du dépôt

```
rapport-commercial-auto/
├── docker-compose.yml
├── .env.example
├── specs/                 # spécifications (lues avant d'écrire du code)
├── data/                  # CSV générés (ignorés par git, sauf échantillon)
├── generator/             # génération des données fictives
├── loader/                # nettoyage + chargement Postgres
├── sql/                   # schéma, vues et requêtes KPI
├── n8n/                   # workflow exporté en JSON
└── docs/                  # schéma du flux, capture du mail
```

## Limites assumées

- Données entièrement fictives, aucun lien avec un vrai ERP.
- Démo locale uniquement (pas d'hébergement).
- Pas d'authentification multi-utilisateurs ni de volumétrie réaliste : ce
  projet démontre un mécanisme, pas un produit prêt pour la production.
