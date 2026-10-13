# 00 — Vision et contraintes

**Statut :** Approved

## Objectif

Démontrer, sous forme de projet portfolio, l'automatisation d'un rapport commercial
quotidien : un fichier de ventes (type export d'ERP) est nettoyé, chargé, agrégé
en SQL et envoyé par mail chaque matin sans intervention humaine.

## Scénario (fictif)

PME de commerce de gros. Le directeur commercial perd 20-30 min chaque matin à
exporter l'ERP et mettre les chiffres en forme. Cible : mail automatique à 7h30
avec les KPI de la veille.

## Périmètre

- Données 100 % fictives, générées par script.
- Tout tourne en local via `docker compose` (décision prise : pas de VPS).
- Trois services : PostgreSQL (stockage), n8n (orchestration), Mailpit (réception
  du mail en local, pour la capture d'écran).

## Répartition des responsabilités (contrainte de design)

- **Python** : génération des données fictives, nettoyage, chargement en base.
  Aucune logique d'orchestration ou de mise en forme du mail ici.
- **n8n** : déclenchement planifié, requêtes SQL, assemblage et envoi du mail,
  gestion de la branche d'erreur. Aucune logique métier cachée dans un script
  Python appelé par n8n — les KPI doivent être visibles comme des requêtes SQL
  dans les nœuds Postgres.

Cette séparation est un critère de qualité du projet : si toute la logique est
en Python, n8n n'est qu'un décorum et le projet ne démontre plus ce qu'il doit
démontrer.

## Hors périmètre (non-goals)

- Pas d'authentification multi-utilisateurs, pas de vrai ERP, pas d'envoi de
  mail réel à des destinataires externes.
- Pas de dashboard interactif (le "produit" est le mail, pas un BI tool).
- Pas de scalabilité / volumétrie réaliste : quelques mois de données suffisent.

## Honnêteté du portfolio

- Mentionner explicitement « projet démo, données fictives » dans le README.
- Le temps gagné est une hypothèse de scénario, présentée comme telle
  (ex. « scénario type : 20 min/jour × 220 jours ≈ 73 h/an »), jamais comme un
  résultat mesuré.

## Critères de réussite globaux

- [ ] `docker compose up` lance Postgres, n8n et Mailpit sans erreur.
- [ ] Le générateur produit un CSV réaliste et un historique de 2 à 3 mois.
- [ ] Le chargement est idempotent (vérifié en rejouant deux fois).
- [ ] Le workflow n8n envoie le mail à 7h30 avec tous les KPI définis dans
  [01-data-generator.md](01-data-generator.md) / [03-sql-kpis.md](03-sql-kpis.md).
- [ ] La branche d'erreur envoie une alerte si le fichier est absent ou vide.
- [ ] Le mail est lisible en 30 secondes.
- [ ] README, schéma du flux et capture du mail sont prêts pour le profil Malt.

## Risques identifiés

- Dérive de scope : enrichir le mail/les KPI indéfiniment. → Limiter aux KPI
  listés dans la spec 01 et 03, pas d'ajout sans mise à jour de la spec.
- Logique métier qui migre en Python par facilité. → Revue explicite à la fin
  de la spec 04 pour vérifier la répartition des responsabilités.
