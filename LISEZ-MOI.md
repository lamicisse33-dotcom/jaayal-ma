# Jaayal Ma Lii — les annonces de Dakar validées par KHALAM

Site statique (GitHub Pages) servi sur **jaayalma.khalam.app**. Le site EST la base des annonces :
`annonces.json` est ce que Bia Xarit lit, les pages `a/*.html` sont les annonces, `r/*.html` les six rubriques.

- Rien n'est publié sans validation par KHALAM : le serveur de Bia (app.khalam.app) reçoit les dépôts
  (site ou « Bia, Jaayal Ma Lii »), les garde en attente, et n'écrit dans ce dépôt qu'après le « ok » de KHALAM.
- `outils-generer.py` régénère toutes les pages à partir de `annonces.json` (à faire tourner après chaque ajout).
- L'action `.github/workflows/expiration.yml` retire chaque nuit les annonces dont la date `expire` est passée.
- Tarifs (17 novembre 2026) : Normale 1 000 F / 7 jours, Prioritaire 2 000 F, Premium 3 500 F ; forfait pro 15 000 F/mois.
- État : site en préparation, annonces d'exemple, `noindex` tant que les vraies annonces ne sont pas là.
