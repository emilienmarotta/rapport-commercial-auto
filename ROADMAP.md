# Roadmap

Découpage en milestones, dans l'ordre d'implémentation. Chaque milestone est
livré via une branche dédiée et une pull request (voir [CLAUDE.md](CLAUDE.md)
pour le workflow Git).

- [x] **M0 — Squelette + environnement.** `docker-compose.yml` (Postgres,
  n8n, Mailpit), `.env.example`, `.gitignore`, README initial, specs/.
- [x] **M1 — Générateur de données fictives.** CSV façon export ERP,
  historique de 2-3 mois, modes d'anomalie. Spec :
  [specs/01-data-generator.md](specs/01-data-generator.md).
- [ ] **M2 — Chargement Postgres.** Nettoyage léger + chargement idempotent
  dans `raw_ventes`. Spec : [specs/02-data-loader.md](specs/02-data-loader.md).
- [ ] **M3 — Requêtes SQL des KPI.** Une vue par bloc du rapport (CA veille,
  comparaisons, top clients/produits, CA région, alerte chute). Spec :
  [specs/03-sql-kpis.md](specs/03-sql-kpis.md).
- [ ] **M4 — Workflow n8n.** Planification 7h30, nœuds Postgres, assemblage
  et envoi du mail, branche d'erreur. Spec :
  [specs/04-n8n-workflow.md](specs/04-n8n-workflow.md).
- [ ] **M5 — Template du mail.** HTML sobre, lisible en 30 secondes, bonus
  graphique. Spec : [specs/05-email-template.md](specs/05-email-template.md).
- [ ] **M6 — Livrables portfolio.** Capture mail, schéma du flux, README
  final. Spec : [specs/06-deliverables.md](specs/06-deliverables.md).

Détail des exigences et critères d'acceptation de chaque milestone :
[specs/](specs/) (voir [specs/README.md](specs/README.md) pour le statut de
chaque spec).
