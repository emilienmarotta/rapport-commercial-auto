# CLAUDE.md

Contexte et conventions de ce projet, pour que les prochaines sessions
Claude Code reprennent sans réexpliquer.

## Projet

Projet portfolio fictif (profil Malt, data engineer) : automatisation d'un
rapport commercial quotidien envoyé par mail. Données 100 % fictives.
Vision complète : [specs/00-vision.md](specs/00-vision.md).

## Méthode : specs-driven

Chaque fonctionnalité a une spec dans [specs/](specs/) **écrite et validée
avant d'être codée**. Ne pas coder en dehors d'une spec existante ; si le
besoin évolue, mettre à jour la spec en premier, puis le code. Statuts :
`Draft` → `Approved` → `Implemented` (champ en haut de chaque fichier spec,
et dans [specs/README.md](specs/README.md)).

## Roadmap

Milestones dans [ROADMAP.md](ROADMAP.md), un par grande brique
(environnement, générateur, loader, SQL, n8n, mail, livrables).

## Contrainte de design critique

Répartition stricte des responsabilités (voir
[specs/00-vision.md](specs/00-vision.md)) :
- **Python** : génération des données, nettoyage, chargement en base.
- **n8n** : planification, requêtes SQL, assemblage/envoi du mail, gestion
  d'erreur.

Ne jamais faire migrer une agrégation métier (KPI) vers un script Python ou
un nœud Code n8n : elle doit rester une vue/requête SQL visible dans un nœud
Postgres. C'est un critère de qualité du projet, pas un détail d'implémentation.

## Stack

Docker Compose (Postgres 16, n8n, Mailpit), Python (venv à la racine du
projet : `.venv/`), SQL. Pas d'hébergement : tout tourne en local.

## Workflow Git

- Jamais de commit ni de push direct sur `main`.
- Une branche par milestone : `milestone/m{N}-{slug}` (ex.
  `milestone/m2-loader-postgres`).
- À la fin d'un milestone : commit, push de la branche, ouverture d'une PR
  vers `main` avec `gh pr create`.
- Quand l'utilisateur confirme que la PR a été mergée (sur GitHub) :
  `git checkout main && git pull && git branch -d <branche>`. La branche
  distante est supprimée automatiquement au merge (option
  `delete_branch_on_merge` activée sur le repo) ; sinon, la supprimer
  explicitement (`git push origin --delete <branche>`).
- Dépôt GitHub public (`emilienmarotta/rapport-commercial-auto`), aucun
  secret commité (`.env` est ignoré, seul `.env.example` est versionné).

## Honnêteté du contenu

Rappeler partout où c'est pertinent (README, mails, code) que les données
sont fictives et que tout gain de temps annoncé est une hypothèse de
scénario, jamais un résultat mesuré (cf. spec 00).
