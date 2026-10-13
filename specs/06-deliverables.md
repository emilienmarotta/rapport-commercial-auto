# 06 — Livrables portfolio Malt

**Statut :** Approved
**Dépend de :** toutes les specs précédentes (projet fonctionnel de bout en bout)

## Objectif

Rendre le projet présentable sur un profil Malt : un visiteur doit comprendre
le problème, la solution et le résultat sans lancer le code.

## Exigences fonctionnelles

- **Capture du mail reçu**, via l'interface web de Mailpit, dans `docs/`.
- **Schéma du flux** (CSV → Python → Postgres → n8n → Mail), fait avec
  Excalidraw ou équivalent, exporté en PNG dans `docs/`.
- **3 lignes sur le temps gagné**, présentées explicitement comme une
  hypothèse de scénario (cf. spec 00 — honnêteté), pas comme un résultat
  mesuré.
- **README** final, structuré pour un lecteur non technicien puis un lecteur
  technique :
  1. Contexte/problème (3-5 lignes).
  2. Solution (1 paragraphe + schéma).
  3. Ce que ça démontre techniquement (stack, répartition Python/n8n).
  4. Comment relancer la démo (`docker compose up` + commandes).
  5. Limites assumées (données fictives, pas de vrai ERP).
- Dépôt Git public, `.env` absent du dépôt, `.env.example` présent et
  documenté.

## Critères d'acceptation

- [ ] Toutes les cases de la section "Critères de réussite globaux" de
  [00-vision.md](00-vision.md) sont cochées.
- [ ] `git log` ne contient aucun secret (vérifier avant le premier push).
- [ ] Un lecteur qui ne connaît pas le projet comprend, en lisant uniquement
  le README, ce que fait le projet et pourquoi — sans lire le code.
- [ ] Le dépôt est public et le README affiche correctement les images
  (schéma, capture mail) depuis GitHub.
