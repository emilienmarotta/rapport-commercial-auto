# 05 — Template du mail

**Statut :** Implemented
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
  - **Décision d'implémentation :** retenu un mini-graphique en barres fait
    uniquement en HTML/CSS (largeur d'un `<div>` proportionnelle au CA de
    chaque région), plutôt que matplotlib ou QuickChart. Ça évite d'ajouter
    une dépendance réseau vers un service de chart hébergé externe (cohérent
    avec le fonctionnement 100 % local de la démo) et un nouvel endpoint
    Python juste pour ce bonus. Conséquence positive sur le critère
    d'acceptation « lisible sans le graphique bonus » : il n'y a pas d'image
    chargée séparément, donc pas de mode de dégradation à gérer.
- Mail d'alerte technique (branche erreur, spec 04) : gabarit distinct,
  minimal — raison de l'échec, pas de chiffres.

## Contrat d'interface

- Le HTML est généré à partir des résultats des vues SQL (spec 03), assemblé
  dans un nœud Code/HTML n8n (spec 04). Pas de dépendance à un template
  engine externe si évitable (concatenation HTML simple ok pour ce projet).

## Critères d'acceptation

- [x] Un œil non technicien comprend le CA de la veille et sa tendance en
  moins de 30 secondes (test informel : montrer le mail à quelqu'un). Le
  CA de la veille est affiché en gros (34px) en haut du mail, suivi
  immédiatement des deux comparaisons avec flèche et pourcentage.
- [x] Les flèches de variation sont correctement colorées selon le signe
  (vert `#1a7f37` si `ecart_valeur >= 0`, rouge `#c0392b` sinon). Vérifié
  avec les données réelles du jour (J-7 et moyenne du mois toutes deux en
  baisse, flèches ▼ rouges).
- [x] Le mail reste lisible sans le graphique bonus (dégradation propre si
  l'image ne charge pas). Le graphique bonus est en HTML/CSS inline (pas
  d'image externe), donc aucun mode de dégradation à tester.
- [x] Le mail d'alerte technique est visuellement distinct du rapport
  normal. Gabarit dédié : bandeau plein rouge en en-tête, aucun tableau ni
  chiffre, uniquement la raison de l'échec.
