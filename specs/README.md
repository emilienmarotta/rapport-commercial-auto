# Specs — rapport-commercial-auto

Méthode : chaque fonctionnalité a une spec écrite et validée avant d'être codée.
Une spec ne change pas en cours d'implémentation sans être mise à jour ici en premier.

Statut possible : `Draft` (à valider) · `Approved` (prête à implémenter) · `Implemented` (code conforme livré).

| Spec | Domaine | Statut |
|---|---|---|
| [00-vision.md](00-vision.md) | Vision, contraintes, critères de réussite globaux | Approved |
| [01-data-generator.md](01-data-generator.md) | Générateur de CSV fictif | Implemented |
| [02-data-loader.md](02-data-loader.md) | Chargement Postgres idempotent | Implemented |
| [03-sql-kpis.md](03-sql-kpis.md) | Vues / requêtes KPI | Approved |
| [04-n8n-workflow.md](04-n8n-workflow.md) | Orchestration n8n + branche d'erreur | Approved |
| [05-email-template.md](05-email-template.md) | Template du mail | Approved |
| [06-deliverables.md](06-deliverables.md) | Livrables portfolio Malt | Approved |

Ordre d'implémentation recommandé : 00 → 01 → 02 → 03 → 04 → 05 → 06
(chaque spec consomme le contrat produit par la précédente).
