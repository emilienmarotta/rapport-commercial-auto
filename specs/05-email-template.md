# 05 — Template du mail

**Statut :** Approved
**Dépend de :** [03-sql-kpis.md](03-sql-kpis.md), [04-n8n-workflow.md](04-n8n-workflow.md)

## Objectif

Un mail HTML sobre, compréhensible en 30 secondes par un directeur commercial
non technicien.

## Exigences fonctionnelles

- Bloc "chiffre clé" : CA de la veille, en grand.
- Flèches/couleur de variation pour la comparaison J-7 et vs moyenne du mois
  (▲ vert si hausse, ▼ rouge si baisse).
- Petit tableau Top 5 clients, petit tableau Top 5 produits.
- Bloc CA par région (tableau ou liste, pas de graphique obligatoire ici).
- Bandeau d'alerte visuel si `kpi_alerte_chute` est vrai (ex. fond rouge/orange
  en haut du mail), même dans le mail "normal" si la chute ne déclenche pas la
  branche d'erreur technique mais reste un signal business.
- Bonus (non bloquant) : un graphique (image) généré via matplotlib ou
  QuickChart, embarqué en pièce jointe ou en image hébergée/inline (CID).
- Mail d'alerte technique (branche erreur, spec 04) : gabarit distinct,
  minimal — raison de l'échec, pas de chiffres.

## Contrat d'interface

- Le HTML est généré à partir des résultats des vues SQL (spec 03), assemblé
  dans un nœud Code/HTML n8n (spec 04). Pas de dépendance à un template
  engine externe si évitable (concatenation HTML simple ok pour ce projet).

## Critères d'acceptation

- [ ] Un œil non technicien comprend le CA de la veille et sa tendance en
  moins de 30 secondes (test informel : montrer le mail à quelqu'un).
- [ ] Les flèches de variation sont correctement colorées selon le signe.
- [ ] Le mail reste lisible sans le graphique bonus (dégradation propre si
  l'image ne charge pas).
- [ ] Le mail d'alerte technique est visuellement distinct du rapport normal.
