# FX Lab Démo — appli installable (PWA)

Labo éducatif **30 jours** pour Dave (Infinix, français) : signaux FX / or / crypto, copie **uniquement sur Exness DÉMO**.  
Pas un conseil financier. Pas d’argent réel. Pas de Play Store. Pas de clé API.

Dossier **prêt GitHub Pages** (chemins relatifs). Publier `fx-lab-app/` tel quel, ou copier son contenu vers `/docs` si Pages est réglé sur le dossier docs.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `index.html` | Toute l’UI du labo (étude, Fib, légendes, multi-sources, recalibrage) + boutons PWA |
| `manifest.webmanifest` | Nom, thème sombre, icônes, `display: standalone` |
| `sw.js` | Cache du shell (ouvrir hors-ligne) · **network-only** pour les cours API (jamais mis en cache) |
| `icons/` | PNG 192 / 512 (any + maskable), apple-touch, favicon |
| `404.html` | Redirige vers l’app (Pages) |
| `.nojekyll` | Empêche Jekyll de casser les chemins |

Régénérer les icônes : `python3 scripts/make-icons.py`

## Installer sur Infinix (Chrome)

1. Ouvre l’URL **GitHub Pages HTTPS** dans **Google Chrome** (icône colorée Google).  
   Pas le navigateur XOS, pas Facebook, **pas** `htmlpreview.github.io`.
2. Attends le chargement. En haut : carte **Installer l’appli & alertes**.
3. Tape **Installer l’appli**. Si Chrome propose la boîte d’install, confirme.  
   Sinon : menu **⋮** (haut droite) → **Installer l’application** ou **Ajouter à l’écran d’accueil**.
4. L’icône **FX Lab Démo** apparaît sur l’écran d’accueil. Ouvre-la comme une appli.
5. Tape **Activer les alertes** → **Autoriser**. Un test EURUSD / ACHAT part tout de suite.  
   Tu peux retester avec **Tester une alerte**.

Si Chrome bloque les notifs : Paramètres Android → Applications → Chrome → Notifications → autoriser.

## Alertes — honnêteté

Quand un **nouveau signal** est généré (pas les « rattrapage » éducatifs), l’appli envoie une notification locale :

- paire
- **ACHAT** ou **VENTE**
- rappel **SL**
- action *Ouvrir pour copier en démo*

Si la permission est refusée ou indisponible : **toast** dans la page + **vibreur** + **bip**.

**Ce n’est pas un push 24h/24 écran éteint.** Ça demanderait un serveur plus tard.  
Cette version alerte **quand l’appli ou l’onglet peut encore tourner** (premier plan, ou arrière-plan Android selon l’OS — Chrome peut geler la page). Le service worker peut afficher la notif si la page a encore le droit de s’exécuter.

## GitHub Pages vs htmlpreview

| Ouverture | PWA (install + SW + notifs système) |
| --- | --- |
| `https://daveblessing.github.io/…/fx-lab-app/` | **Oui** — à utiliser |
| Dossier `docs/` en racine Pages | **Oui** (copier le contenu de ce dossier) |
| `htmlpreview.github.io/…` | **Non** — mauvais origine / périmètre SW |
| `raw.githubusercontent.com` | **Non** |
| Fichier `file://` | **Non** (SW interdit) |

Réglage Pages typique : *Settings → Pages → Deploy from branch → `/docs`* (après copie) **ou** laisser ce dossier en sous-chemin `/fx-lab-app/`. Les URLs du manifest et du SW sont **relatives**, les deux marchent.

Aucun `git push` n’est fait ici ; à publier ensuite.

## Changelog (FR)

- **Fraîcheur cours** : polling ∼12–15s (visible) / ∼45–60s (onglet caché) ; Mode turbo ∼8–10s (ON par défaut si focus) ; badge « À jour : il y a Xs » (rouge si >90s) ; bouton **Actualiser maintenant** ; flash léger des prix à chaque MAJ OK ; SW v3 network-only pour les API quotes. Limite honnête : pas de ticks ms Exness sans flux broker/serveur — max possible avec API publiques gratuites en PWA.
- **PWA** : manifest + icônes + service worker, « Installer l’appli », « Activer les alertes », notifications locales, fallback toast/vibreur/bip.
- Conservé : étude 30 jours, boîte Fib / structure / légendes, or+crypto+indices, consensus multi-sources, bannières DÉMO, recalibrage, checklist copie Exness démo.
- Rappel : Fib n’est pas magique · pas de garantie · démo seulement.

## Hors-ligne

Le **shell** (UI) peut se réouvrir sans réseau. Les **cours** restent en **network-only** (jamais mis en cache par le SW) : sans API, les prix ne se mettent pas à jour (message d’erreur habituel). Aucune donnée broker, aucun mot de passe.

## Nouveautés toolkit (démo)

- **Suivi copies** — « Copié » ouvre un tracker (Gagné / Perdu / Fermé) qui alimente le recalibrage.
- **RSI (14) + EMA (20/50)** — historique local ; carte signal + panneau Indicateurs ; boost léger de confiance si alignement.
- **Calendrier éco** — modèle high-impact semaine + liens ForexFactory / Investing ; filtre ±30 min optionnel.
- **Astuces notif Android** — arrière-plan, batterie, notifications ; 24/7 écran éteint = serveur plus tard.
- Honnêteté inchangée : DÉMO only · pas de Play Store · pas d’API broker.

