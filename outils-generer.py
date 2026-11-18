#!/usr/bin/env python3
# Jaayal ma — générateur du site statique à partir d'annonces.json.
# Produit : index.html, recherche.html, r/<fenetre>.html (6 rubriques), a/<id>.html (une page par annonce).
# Tout le style est ici : les six rubriques et toutes les annonces partagent exactement le même squelette.
import json, html, re, datetime, os

PREPARATION = True   # True = noindex + bandeau « Site en préparation ». Passer à False quand les vraies annonces remplacent les exemples.
SITE = "https://jaayalma.khalam.app"

D = json.load(open('annonces.json', encoding='utf-8')); A = D['annonces']
E = html.escape
def F(n): return f"{n:,}".replace(",", " ") + " F"
def slug(x): return re.sub(r"[^a-z0-9]+", "-", x.lower().replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ô","o").replace("&","")).strip("-")
def dmy(s): return f"{s[8:10]}/{s[5:7]}/{s[:4]}"
NIV = {"premium": "Premium", "prioritaire": "Prioritaire", "normale": ""}
RANG = {"premium": 0, "prioritaire": 1, "normale": 2}
TYPE = {"vente": "À vendre", "location": "À louer"}

# ── Les six fenêtres (identiques à FENETRES dans lib/jaayalma.ts côté serveur) ─────────────────
FENETRES = [
 ("immobilier","Immobilier","Vente et location : maisons, appartements, chambres, terrains, commerces et locaux.",["Vente","Location"]),
 ("vehicules","Véhicules","Voitures, motos et scooters, location de voitures, pièces et pneus.",["Voitures","Motos & scooters","Location de voitures","Pièces & pneus"]),
 ("electromenager","Électroménager & maison","Frigos, machines, ventilateurs, télés, téléphones, ordinateurs, meubles, cuisine.",["Électroménager","Télé, téléphones & ordinateurs","Meubles & décoration","Cuisine & ustensiles"]),
 ("mode","Mode & bijoux","Vide-dressing (habits), bijoux et montres, tissus et bazin, beauté.",["Vide-dressing","Bijoux & montres","Tissus & bazin","Beauté & mèches"]),
 ("animaux","Animaux","Moutons de Tabaski, bœufs et chèvres, volailles, chiens et chats.",["Moutons","Bœufs & chèvres","Volailles","Chiens & chats"]),
 ("services","Services & divers","Services, emplois, événements, sport et loisirs, bébé et enfants, matériel pro.",["Services","Emplois","Événements (chaises, bâches, sono)","Sport & loisirs","Bébé & enfants","Matériel pro & BTP"]),
]
FEN = {k: (n, d, s) for k, n, d, s in FENETRES}
# repli pour les annonces d'exemple qui n'auraient pas encore fenetre/sous
MAP={'villa-almadies-4ch':'immobilier','appart-mermoz-3p':'immobilier','chambre-pikine-rue10':'immobilier','maison-keur-massar':'immobilier','terrain-rufisque-300':'immobilier','boutique-sacre-coeur':'immobilier','restaurant-ngor-cession':'immobilier','tucson-2021-dakar':'vehicules','corolla-2018-pikine':'vehicules','peugeot-308-ouakam':'vehicules','tv-samsung-55':'electromenager','ventilateur-binatone':'electromenager','frigo-hisense-2-portes':'electromenager','grand-boubou-bazin':'mode','montre-homme-cuir':'mode','collier-or-18k':'mode'}
PARTIE={'villa-almadies-4ch':'Vente','maison-keur-massar':'Vente','terrain-rufisque-300':'Vente','restaurant-ngor-cession':'Vente','appart-mermoz-3p':'Location','chambre-pikine-rue10':'Location','boutique-sacre-coeur':'Location','tucson-2021-dakar':'Voitures','corolla-2018-pikine':'Voitures','peugeot-308-ouakam':'Voitures','tv-samsung-55':'Télé, téléphones & ordinateurs','ventilateur-binatone':'Électroménager','frigo-hisense-2-portes':'Électroménager','grand-boubou-bazin':'Vide-dressing','montre-homme-cuir':'Bijoux & montres','collier-or-18k':'Bijoux & montres'}
for a in A:
    a['fenetre'] = a.get('fenetre') or MAP.get(a['id'], 'services'); a['sous'] = a.get('sous') or PARTIE.get(a['id'], '')
    a.setdefault('photos', []); a.setdefault('surface', ''); a.setdefault('titre_wo', ''); a.setdefault('pro', False); a.setdefault('unite', ''); a.setdefault('etat', ''); a.setdefault('details', {}); a.setdefault('vendeur', '')
    a['page'] = f"{SITE}/a/{a['id']}.html"; a['image'] = f"{SITE}/img/{a['photos'][0]}" if a['photos'] else ''
def classer(liste): return sorted(liste, key=lambda a: (RANG.get(a['niveau'], 2), a.get('depuis', '')), reverse=False) and sorted(liste, key=lambda a: (RANG.get(a['niveau'], 2), -int(a.get('depuis', '2000-01-01').replace('-', ''))))
A = classer(A)

# ── Style commun ──────────────────────────────────────────────────────────────────────────────
CSS = '''<style>
:root{--bg:#F4F2EC;--carte:#FFFFFF;--fg:#141B2D;--doux:#5A6275;--ligne:#E3DED3;--marine:#0B1F4D;--marine2:#163070;--or:#C9A227;--or-fond:#FBF3DC;--prio:#1E4FB8;--prio-fond:#E6EEFF;--wa:#1EBE5D;--vert-fond:#E8F8EE;--ombre:0 1px 2px rgba(20,27,45,.06),0 6px 20px -12px rgba(20,27,45,.25);
 --display:"Space Grotesk","Inter",system-ui,sans-serif;--texte:"Inter",system-ui,-apple-system,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0E1322;--carte:#171E33;--fg:#EEF0F6;--doux:#A3AAC0;--ligne:#2A3350;--or:#E2BC45;--or-fond:#3A2F10;--prio:#7FA4FF;--prio-fond:#1B2A52;--vert-fond:#13311F;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0E1322;--carte:#171E33;--fg:#EEF0F6;--doux:#A3AAC0;--ligne:#2A3350;--or:#E2BC45;--or-fond:#3A2F10;--prio:#7FA4FF;--prio-fond:#1B2A52;--vert-fond:#13311F;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--texte);font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit}img{max-width:100%}
.int{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));max-width:1120px;margin:0 auto}
/* bandeau préparation */
.maquette{background:var(--or-fond);color:var(--fg);font-size:13px;text-align:center;padding:7px 16px}
/* entête */
.bande{background:var(--marine);color:#fff}
.bande .int{padding-block:12px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.marque{display:flex;align-items:baseline;gap:9px;text-decoration:none;white-space:nowrap}
.marque b{font-family:var(--display);font-size:24px;letter-spacing:-.01em}
.marque span{font-size:11.5px;color:var(--or);letter-spacing:.08em;text-transform:uppercase}
.cherche{flex:1 1 240px;display:flex;background:#fff;border-radius:12px;overflow:hidden;min-width:0}
.cherche input{flex:1;border:0;padding:11px 14px;font:inherit;font-size:15px;min-width:0;color:#141B2D;background:#fff}
.cherche input:focus{outline:none}
.cherche button{border:0;background:var(--or);color:#141B2D;font:inherit;font-weight:700;padding:0 16px;cursor:pointer}
.bdeposer{background:var(--or);color:#141B2D;text-decoration:none;font-weight:700;padding:11px 16px;border-radius:12px;white-space:nowrap;font-size:14.5px}
.bdeposer:hover{filter:brightness(1.05)}
/* ruban des rubriques, identique sur toutes les pages */
.ruban{background:var(--carte);border-bottom:1px solid var(--ligne)}
.ruban .int{display:flex;gap:6px;overflow-x:auto;padding-block:8px;scrollbar-width:none}
.ruban .int::-webkit-scrollbar{display:none}
.ruban a{flex:0 0 auto;text-decoration:none;font-size:13.5px;font-weight:500;padding:7px 13px;border-radius:999px;border:1px solid transparent;color:var(--doux)}
.ruban a:hover{border-color:var(--ligne);color:var(--fg)}
.ruban a[aria-current]{background:var(--marine);color:#fff}
/* fil + titres */
.fil{font-size:13px;color:var(--doux);margin:16px 0 4px;display:flex;gap:6px;flex-wrap:wrap}
.fil a{text-decoration:none}.fil a:hover{text-decoration:underline}
.tete{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:0 0 6px}
h1{font-family:var(--display);font-size:clamp(24px,4vw,34px);line-height:1.12;margin:0;letter-spacing:-.015em;text-wrap:balance}
.tete .n{color:var(--doux);font-size:14px;font-variant-numeric:tabular-nums}
.sous-titre{color:var(--doux);margin:0 0 14px;max-width:70ch}
/* filtres */
.filtres{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--ligne);margin-bottom:16px}
.filtres .int{padding-block:10px;display:flex;flex-direction:column;gap:8px}
.puces{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.puces::-webkit-scrollbar{display:none}
.puces button{flex:0 0 auto;border:1px solid var(--ligne);background:var(--carte);color:var(--fg);border-radius:999px;padding:6px 13px;font:inherit;font-size:13.5px;cursor:pointer}
.puces button[aria-pressed="true"]{background:var(--marine);color:#fff;border-color:var(--marine)}
.puces button i{font-style:normal;color:var(--doux);font-size:12px;margin-left:5px}
.puces button[aria-pressed="true"] i{color:#C9D3F0}
.outils{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.outils select,.outils input{border:1px solid var(--ligne);background:var(--carte);color:var(--fg);border-radius:10px;padding:7px 10px;font:inherit;font-size:13.5px;min-width:0}
.outils input{width:110px}
.outils .prixg{display:flex;align-items:center;gap:6px;color:var(--doux);font-size:13px}
.outils .compte{margin-left:auto;color:var(--doux);font-size:13px;font-variant-numeric:tabular-nums}
.outils .raz{border:0;background:none;color:var(--prio);font:inherit;font-size:13px;cursor:pointer;text-decoration:underline;padding:0}
/* grille et cartes — la même partout */
main{padding-block:0 40px}
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
@media (max-width:560px){.grille{grid-template-columns:repeat(2,1fr);gap:10px}}
.carte{background:var(--carte);border:1px solid var(--ligne);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;min-width:0;text-decoration:none;position:relative;box-shadow:var(--ombre)}
.carte.premium{border-color:var(--or);box-shadow:0 0 0 2px var(--or-fond),var(--ombre)}
.carte .visuel{position:relative;background:#E9E6DD}
.carte .visuel img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
.carte .visuel .nophoto{aspect-ratio:4/3;display:grid;place-items:center;color:var(--doux);font-size:13px}
.badge{position:absolute;top:8px;left:8px;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:4px 8px;border-radius:999px}
.badge.premium{background:var(--or);color:#141B2D}.badge.prioritaire{background:var(--prio);color:#fff}
.type{position:absolute;top:8px;right:8px;font-size:11px;background:rgba(11,31,77,.85);color:#fff;padding:4px 8px;border-radius:999px}
.nbph{position:absolute;bottom:8px;right:8px;font-size:11.5px;background:rgba(0,0,0,.55);color:#fff;padding:3px 7px;border-radius:999px}
.corps{padding:10px 12px 12px;display:flex;flex-direction:column;gap:4px;flex:1}
.prix{font-family:var(--display);font-size:18px;font-weight:700;letter-spacing:-.01em;font-variant-numeric:tabular-nums}
.prix small{font-family:var(--texte);font-weight:500;font-size:12.5px;color:var(--doux)}
.titre{font-weight:600;line-height:1.3;font-size:14.5px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.wo{color:var(--doux);font-size:12.5px}
.attrs{display:flex;flex-wrap:wrap;gap:4px;margin-top:2px}.attrs span b{font-weight:600;color:var(--fg)}.attrs span{font-size:11.5px;color:var(--doux);background:var(--bg);border:1px solid var(--ligne);border-radius:6px;padding:2px 7px}
.carte .par{font-size:12px;color:var(--doux)}
.meta{display:flex;justify-content:space-between;gap:8px;color:var(--doux);font-size:12px;margin-top:auto;padding-top:6px;border-top:1px solid var(--ligne)}
.meta b{color:var(--fg);font-weight:600}
.meta .pro{color:var(--prio);font-weight:600}
.vide{background:var(--carte);border:1px dashed var(--ligne);border-radius:14px;padding:28px 18px;text-align:center;color:var(--doux);grid-column:1/-1}
.vide b{display:block;color:var(--fg);font-family:var(--display);font-size:17px;margin-bottom:4px}
.vide a{color:var(--prio)}
/* sections de l'accueil */
.hero{padding-block:28px 10px}
.hero h1{font-size:clamp(26px,4.6vw,42px)}
.hero h1 em{font-style:normal;color:var(--or)}
.hero p{margin:8px 0 0;color:var(--doux);max-width:62ch}
.dire{margin-top:14px;display:inline-flex;align-items:center;gap:10px;background:var(--carte);border:1px solid var(--ligne);border-radius:999px;padding:8px 14px 8px 10px;font-size:14px}
.dire i{width:30px;height:30px;border-radius:50%;background:var(--or);display:inline-grid;place-items:center;color:#141B2D;font-style:normal;font-weight:700;font-family:var(--display)}
h2.sec{font-family:var(--display);font-size:21px;margin:26px 0 12px;letter-spacing:-.01em;display:flex;align-items:baseline;justify-content:space-between;gap:10px}
h2.sec a{font:500 13.5px var(--texte);color:var(--prio);text-decoration:none}
.fenetres{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
@media (max-width:560px){.fenetres{grid-template-columns:repeat(2,1fr);gap:10px}}
.fenetre{background:var(--carte);border:1px solid var(--ligne);border-radius:14px;padding:14px 14px 12px;text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px;min-width:0;box-shadow:var(--ombre)}
.fenetre b{font-family:var(--display);font-size:16px;line-height:1.2}
.fenetre span{font-size:12.5px;color:var(--doux);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.fenetre .n{margin-top:auto;padding-top:8px;font-size:12.5px;color:var(--prio);font-weight:600;display:flex;justify-content:space-between}
.fenetre .n em{font-style:normal;color:var(--doux);font-weight:500}
.fenetre .apercu{display:flex;gap:5px;margin-top:2px}
.fenetre .apercu img{width:48px;height:36px;object-fit:cover;border-radius:6px;border:1px solid var(--ligne)}
.tarifs{margin-top:34px;background:var(--carte);border:1px solid var(--ligne);border-radius:16px;padding:22px}
.tarifs h2,.comment h2{font-family:var(--display);margin:0 0 6px;font-size:22px;letter-spacing:-.01em}
.tarifs p{color:var(--doux);margin:0 0 14px}
.tarifs table{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
.tarifs th,.tarifs td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--ligne)}
.tarifs th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--doux);font-weight:600}
.tarifs td:nth-child(n+2),.tarifs th:nth-child(n+2){text-align:right;white-space:nowrap}
.tarifs tr.premium td:first-child{color:var(--or);font-weight:700}
.tarifs tr.prioritaire td:first-child{color:var(--prio);font-weight:700}
.tarifs .note{font-size:13px;color:var(--doux);margin:12px 0 0}
.comment{margin-top:26px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.comment>div{background:var(--carte);border:1px solid var(--ligne);border-radius:14px;padding:16px}
.comment h2{grid-column:1/-1;margin-bottom:0}
.comment b{display:block;font-family:var(--display);font-size:16.5px;margin-bottom:4px}
.comment p{margin:0;color:var(--doux);font-size:14px}
.appel{margin-top:26px;background:var(--marine);color:#fff;border-radius:16px;padding:20px 22px;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.appel b{font-family:var(--display);font-size:19px;display:block}
.appel span{color:#C9D3F0;font-size:14px}
footer{padding-block:22px 30px;color:var(--doux);font-size:13px;border-top:1px solid var(--ligne);margin-top:30px}
footer .int{display:flex;gap:10px 22px;flex-wrap:wrap;justify-content:space-between}
footer a{color:var(--doux)}
/* page annonce */
.fiche{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:24px;align-items:start;padding-block:0 40px}
@media (max-width:860px){.fiche{grid-template-columns:1fr}}
.galerie{border-radius:16px;overflow:hidden;border:1px solid var(--ligne);background:#E9E6DD;position:relative}
.galerie .grande{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
.galerie .nophoto{aspect-ratio:4/3;display:grid;place-items:center;color:var(--doux)}
.vignettes{display:flex;gap:8px;margin-top:8px}
.vignettes img{width:84px;height:63px;object-fit:cover;border-radius:8px;border:2px solid transparent;cursor:pointer}
.vignettes img[aria-current]{border-color:var(--or)}
.fiche h1{margin:14px 0 2px;font-size:clamp(22px,3.6vw,30px)}
.fiche .wo{font-size:15px}
.fiche .ligne-prix{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:8px 0 6px}
.fiche .prix{font-size:28px}
.etiq{font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:4px 9px;border-radius:999px;background:var(--prio-fond);color:var(--prio)}
.etiq.premium{background:var(--or-fond);color:#8A6A0A}.etiq.offre{background:var(--marine);color:#fff}
.repere{color:var(--doux);font-size:13.5px;display:flex;gap:6px 14px;flex-wrap:wrap;margin:0 0 16px}
.repere b{color:var(--fg);font-weight:600}
h2.bloc{font-family:var(--display);font-size:18px;margin:22px 0 8px;letter-spacing:-.01em}
.caract{width:100%;border-collapse:collapse;font-size:14.5px;background:var(--carte);border:1px solid var(--ligne);border-radius:12px;overflow:hidden}
.caract th,.caract td{text-align:left;padding:10px 14px;border-bottom:1px solid var(--ligne)}
.caract tr:last-child th,.caract tr:last-child td{border-bottom:0}
.caract th{font-weight:500;color:var(--doux);width:42%}
.desc{max-width:68ch;white-space:pre-line;margin:0}
.lateral{position:sticky;top:calc(env(safe-area-inset-top,0px) + 12px);display:flex;flex-direction:column;gap:12px}
.vendeur{background:var(--carte);border:1px solid var(--ligne);border-radius:16px;padding:16px;box-shadow:var(--ombre)}
.vendeur .qui{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.vendeur .av{width:42px;height:42px;border-radius:50%;background:var(--marine);color:#fff;display:grid;place-items:center;font-family:var(--display);font-weight:700;font-size:17px}
.vendeur .qui b{display:block;font-size:15px}
.vendeur .qui span{font-size:12.5px;color:var(--doux)}
.bwa{display:flex;justify-content:center;align-items:center;gap:8px;background:var(--wa);color:#fff;text-decoration:none;font-weight:700;padding:13px 16px;border-radius:12px;font-size:15px}
.bwa svg{width:20px;height:20px;fill:currentColor}
.btel{display:flex;justify-content:center;align-items:center;gap:8px;margin-top:8px;border:1px solid var(--ligne);background:var(--bg);color:var(--fg);text-decoration:none;font-weight:600;padding:12px 16px;border-radius:12px;font-variant-numeric:tabular-nums}
.verif{font-size:12.5px;color:var(--doux);display:flex;align-items:flex-start;gap:6px;margin:12px 0 0}
.verif i{flex:0 0 16px;width:16px;height:16px;border-radius:50%;background:var(--or);display:inline-grid;place-items:center;color:#141B2D;font-style:normal;font-size:11px;font-weight:700;margin-top:2px}
.partage{display:flex;gap:8px}
.partage a,.partage button{flex:1;border:1px solid var(--ligne);background:var(--carte);color:var(--fg);border-radius:10px;padding:9px;font:inherit;font-size:13px;text-decoration:none;text-align:center;cursor:pointer}
.securite{background:var(--vert-fond);border-radius:14px;padding:14px 16px;font-size:13.5px}
.securite b{display:block;margin-bottom:4px}
.securite ul{margin:0;padding-left:18px;color:var(--doux)}
.securite li{margin:2px 0}
.signaler{font-size:12.5px;color:var(--doux);text-align:center;display:block}
.cite{font-size:13px;color:#8A6A0A;background:var(--or-fond);border-radius:10px;padding:8px 12px;margin:10px 0 0}
.similaires{grid-column:1/-1}
.carte:focus-visible,.bwa:focus-visible,.puces button:focus-visible,.bdeposer:focus-visible{outline:3px solid var(--prio);outline-offset:2px}
@media (prefers-reduced-motion:no-preference){.carte,.fenetre{transition:transform .15s}.carte:hover,.fenetre:hover{transform:translateY(-2px)}}
</style>'''
HEAD = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap">'
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.6c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.1c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>'

def squelette(titre, desc, corps, prefix, canon):
    robots = '<meta name="robots" content="noindex">' if PREPARATION else ''
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">{robots}
<title>{E(titre)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}/{canon}">
<meta property="og:title" content="{E(titre)}"><meta property="og:description" content="{E(desc)}"><meta property="og:site_name" content="Jaayal ma">
{HEAD}{CSS}
</head><body>
{corps}
</body></html>'''

def entete(prefix, actif=None, q=''):
    bandeau = '<div class="maquette">Site en préparation — les annonces affichées sont des exemples, avec des noms et des numéros fictifs.</div>' if PREPARATION else ''
    ruban = ''.join(f'<a href="{prefix}r/{k}.html"{" aria-current=page" if k==actif else ""}>{E(n)}</a>' for k, n, _, _ in FENETRES)
    return f'''{bandeau}
<header class="bande"><div class="int">
<a class="marque" href="{prefix}index.html"><b>Jaayal ma</b><span>par KHALAM</span></a>
<form class="cherche" action="{prefix}recherche.html" method="get" role="search"><input type="search" name="q" value="{E(q)}" placeholder="Que cherchez-vous ? (ex. frigo, Pikine, Corolla)" aria-label="Rechercher une annonce"><button type="submit">Chercher</button></form>
<a class="bdeposer" href="{prefix}deposer.html">+ Déposer une annonce</a>
</div></header>
<nav class="ruban" aria-label="Rubriques"><div class="int"><a href="{prefix}index.html"{" aria-current=page" if actif=="accueil" else ""}>Accueil</a>{ruban}</div></nav>'''

def pied(prefix):
    return f'''<footer><div class="int"><span>Jaayal ma est un service de <a href="https://khalam.app">KHALAM</a>, Dakar. Annonces publiées sous la responsabilité de leurs auteurs, après validation par KHALAM.</span><span><a href="{prefix}deposer.html">Déposer</a> · <a href="{prefix}index.html#tarifs">Tarifs</a> · <a href="https://khalam.app/bia">Bia Xarit</a> · <a href="{prefix}annonces.json">annonces.json</a></span></div></footer>'''

def attrs(a):
    NUES = {'marque','année','annee','boîte','boite','carburant','kilométrage','kilometrage','taille','matière','matiere','modèle','modele'}
    items = ([E(a['etat'])] if a['etat'] else []) + [E(str(v)) if k.lower() in NUES else f'{E(k)} <b>{E(str(v))}</b>' for k, v in list(a['details'].items())[:3] if v]
    if not items and a['sous']: items = [E(a['sous'])]
    return f'<div class="attrs">{"".join(f"<span>{x}</span>" for x in items)}</div>' if items else ''
def carte(a, prefix):
    niv = NIV.get(a['niveau'], ''); badge = f'<span class="badge {a["niveau"]}">{niv}</span>' if niv else ''
    visuel = f'<img src="{prefix}img/{a["photos"][0]}" alt="{E(a["titre"])}" loading="lazy">' if a['photos'] else '<div class="nophoto">Pas de photo</div>'
    nb = f'<span class="nbph">📷 {len(a["photos"])}</span>' if len(a['photos']) > 1 else ''
    data = f'data-q="{E(a["quartier"])}" data-s="{E(a["sous"])}" data-f="{a["fenetre"]}" data-p="{a["prix"]}" data-d="{a.get("depuis","")}" data-r="{RANG.get(a["niveau"],2)}" data-t="{E((a["titre"]+" "+a["titre_wo"]+" "+a["desc"]+" "+a["quartier"]+" "+a["sous"]).lower())}"'
    return f'''<a class="carte {a['niveau']}" href="{prefix}a/{a['id']}.html" {data}>
<div class="visuel">{visuel}{badge}<span class="type">{TYPE.get(a['type'],'')}</span>{nb}</div>
<div class="corps"><div class="prix">{F(a['prix'])}<small> {E(a['unite'])}</small></div><div class="titre">{E(a['titre'])}</div>{f'<div class="wo">{E(a["titre_wo"])}</div>' if a['titre_wo'] and a['titre_wo']!=a['titre'] else ''}
{attrs(a)}
<div class="meta"><span><b>{E(a['quartier'])}</b>, Dakar</span><span>{'<span class="pro">Pro</span> · ' if a['pro'] else ''}{dmy(a['depuis'])[:5]}</span></div></div></a>'''

def filtres(items, sous, avec_rubrique=False):
    quartiers = sorted(set(a['quartier'] for a in items))
    puces = f'<button type="button" data-s="" aria-pressed="true">Toutes<i>{len(items)}</i></button>' + ''.join(
        f'<button type="button" data-s="{E(x)}" aria-pressed="false">{E(x)}<i>{len([a for a in items if a["sous"]==x])}</i></button>' for x in sous)
    rub = f'<select id="f-f" aria-label="Rubrique"><option value="">Toutes les rubriques</option>{"".join(f"<option value={k}>{E(n)}</option>" for k,n,_,_ in FENETRES)}</select>' if avec_rubrique else ''
    return f'''<div class="filtres"><div class="int">
<div class="puces" id="f-s">{puces if sous else ''}</div>
<div class="outils">{rub}<select id="f-q" aria-label="Quartier"><option value="">Tous les quartiers</option>{''.join(f'<option>{E(q)}</option>' for q in quartiers)}</select>
<span class="prixg">Prix <input id="f-min" type="number" inputmode="numeric" placeholder="min" min="0"> – <input id="f-max" type="number" inputmode="numeric" placeholder="max" min="0"> F</span>
<select id="f-tri" aria-label="Trier"><option value="">Mise en avant, puis récentes</option><option value="recent">Plus récentes</option><option value="prix+">Prix croissant</option><option value="prix-">Prix décroissant</option></select>
<span class="compte" id="f-n"></span><button type="button" class="raz" id="f-raz" hidden>Effacer les filtres</button></div>
</div></div>'''

SCRIPT_FILTRES = '''<script>(function(){
var g=document.getElementById('grille');if(!g)return;var cartes=[].slice.call(g.querySelectorAll('.carte'));var vide=document.getElementById('vide-filtre');
var S=document.getElementById('f-s'),Q=document.getElementById('f-q'),MI=document.getElementById('f-min'),MA=document.getElementById('f-max'),T=document.getElementById('f-tri'),N=document.getElementById('f-n'),R=document.getElementById('f-raz'),FF=document.getElementById('f-f');
var sous='';var q0=new URLSearchParams(location.search).get('q')||'';var qmots=q0.toLowerCase().split(/\\s+/).filter(Boolean);
function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')}
function appliquer(){var n=0;var mi=+MI.value||0,ma=+MA.value||Infinity;
 cartes.forEach(function(c){var ok=(!sous||c.dataset.s===sous)&&(!Q.value||c.dataset.q===Q.value)&&(!FF||!FF.value||c.dataset.f===FF.value)&&(+c.dataset.p>=mi)&&(+c.dataset.p<=ma);
  if(ok&&qmots.length){var t=norm(c.dataset.t);ok=qmots.every(function(m){return t.indexOf(norm(m))>-1})}
  c.hidden=!ok;if(ok)n++});
 var tri=T.value;var vis=cartes.filter(function(c){return !c.hidden});
 vis.sort(function(a,b){if(tri==='prix+')return a.dataset.p-b.dataset.p;if(tri==='prix-')return b.dataset.p-a.dataset.p;if(tri==='recent')return b.dataset.d.localeCompare(a.dataset.d);return (a.dataset.r-b.dataset.r)||b.dataset.d.localeCompare(a.dataset.d)});
 vis.forEach(function(c){g.appendChild(c)});
 N.textContent=n+' annonce'+(n>1?'s':'');if(vide)vide.hidden=n>0;
 var actif=sous||Q.value||MI.value||MA.value||T.value||(FF&&FF.value);R.hidden=!actif;
 if(S)[].forEach.call(S.querySelectorAll('button'),function(b){b.setAttribute('aria-pressed',b.dataset.s===sous?'true':'false')});}
if(S)S.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;sous=b.dataset.s;appliquer();});
[Q,MI,MA,T,FF].forEach(function(el){if(el)el.addEventListener('input',appliquer)});
R.addEventListener('click',function(){sous='';Q.value='';MI.value='';MA.value='';T.value='';if(FF)FF.value='';appliquer();});
if(location.hash){var h=decodeURIComponent(location.hash.slice(1));if(S){var b=[].filter.call(S.querySelectorAll('button'),function(x){return x.dataset.s&&x.dataset.s.toLowerCase().replace(/[^a-z0-9]+/g,'-')===h})[0];if(b)sous=b.dataset.s;}}
appliquer();})();</script>'''

def grille(items, prefix, vide_txt):
    return f'<div class="grille" id="grille">{"".join(carte(a, prefix) for a in items)}<div class="vide" id="vide-filtre" hidden><b>Aucune annonce ne correspond</b>Essayez un autre quartier ou effacez les filtres.</div>{"" if items else vide_txt}</div>'

# ── Accueil ────────────────────────────────────────────────────────────────────────────────────
def tuile(k):
    n, d, s = FEN[k]; items = [a for a in A if a['fenetre'] == k]
    apercu = ''.join(f'<img src="img/{a["photos"][0]}" alt="" loading="lazy">' for a in items[:4] if a['photos'])
    compte = f'{len(items)} annonce{"s" if len(items)>1 else ""}' if items else '<em>Bientôt vos annonces</em>'
    return f'<a class="fenetre" href="r/{k}.html"><b>{E(n)}</b><span>{E(d)}</span>{f"<div class=apercu>{apercu}</div>" if apercu else ""}<div class="n"><span>{compte}</span><span>→</span></div></a>'
TARIFS = '''<section class="tarifs" id="tarifs"><h2>Tarifs</h2><p>Une annonce = 7 jours, payée d’avance par Wave. Plus le niveau est haut, plus l’annonce est vue.</p>
<table><thead><tr><th>Niveau</th><th>7 jours</th><th>+7 jours</th><th>30 jours</th></tr></thead><tbody>
<tr class="premium"><td>Premium — tout en haut de sa rubrique, et Bia la cite en premier à la voix</td><td>3 500 F</td><td>3 500 F</td><td>12 000 F</td></tr>
<tr class="prioritaire"><td>Prioritaire — au-dessus des annonces normales</td><td>2 000 F</td><td>2 000 F</td><td>7 000 F</td></tr>
<tr><td>Normale — dans sa rubrique, par date</td><td>1 000 F</td><td>1 000 F</td><td>3 500 F</td></tr></tbody></table>
<p class="note">Professionnels (agences, courtiers, boutiques, vendeurs de véhicules) : forfait 15 000 F par mois, annonces normales illimitées, Prioritaire et Premium à moitié prix. Pendant le lancement, la première annonce de 7 jours est offerte.</p></section>'''
COMMENT = '''<section class="comment" id="comment"><h2>Comment ça marche</h2>
<div><b>1. Vous payez et recevez un code</b><p>1 000 F par Wave pour 7 jours. Le code JM-XXXX arrive aussitôt et ouvre le formulaire. Pendant le lancement, la première annonce est offerte.</p></div>
<div><b>2. Vous décrivez</b><p>Rubrique, titre, prix, quartier, WhatsApp, 1 à 3 photos. Ou dites simplement « Bia, jaayal ma » : elle remplit tout avec vous, en wolof ou en français.</p></div>
<div><b>3. KHALAM valide</b><p>Rien n’est publié sans relecture : numéro connu, annonce vérifiée. C’est ce qui fait la différence avec un groupe WhatsApp.</p></div>
<div><b>4. On vous contacte</b><p>Votre annonce a sa page, dans sa rubrique, partageable sur WhatsApp. Bia la propose à la voix à ceux qui cherchent dans votre quartier.</p></div></section>'''
recentes = sorted(A, key=lambda a: a.get('depuis', ''), reverse=True)[:8]
index = f'''{entete('', 'accueil')}
<section class="hero int"><h1>Tout se vend à Dakar. Ici, <em>chaque chose a sa page</em>.</h1>
<p>Six rubriques, des annonces relues par KHALAM avant publication, le vendeur joignable sur WhatsApp. Et Bia Xarit les propose à la voix à ceux qui cherchent.</p>
<div class="dire"><i>B</i>Pour déposer : dites <b>« Bia, jaayal ma »</b>, ou <a href="deposer.html" style="font-weight:600">déposez ici</a></div></section>
<main class="int" id="fenetres">
<h2 class="sec">Rubriques</h2><div class="fenetres">{''.join(tuile(k) for k,_,_,_ in FENETRES)}</div>
<h2 class="sec">Dernières annonces <a href="recherche.html">Tout voir →</a></h2>
<div class="grille">{''.join(carte(a, '') for a in recentes) if recentes else '<div class="vide"><b>Pas encore d’annonce</b>Soyez le premier : la première annonce est offerte.</div>'}</div>
{TARIFS}{COMMENT}
<div class="appel"><div><b>Quelque chose à vendre ?</b><span>7 jours en ligne pour 1 000 F, validée par KHALAM, lue par Bia.</span></div><a class="bdeposer" href="deposer.html">+ Déposer une annonce</a></div>
</main>
{pied('')}'''
open('index.html', 'w', encoding='utf-8').write(squelette('Jaayal ma — les annonces de Dakar validées par KHALAM', 'Jaayal ma — les annonces de Dakar validées par KHALAM, rubrique par rubrique : immobilier, véhicules, électroménager, mode et bijoux, animaux, services. Dites « Bia, jaayal ma ».', index, '', ''))

# ── Recherche (toutes les annonces, filtre par mots ?q=) ──────────────────────────────────────
rech = f'''{entete('', None)}
<div class="int"><p class="fil"><a href="index.html">Jaayal ma</a> › Recherche</p><div class="tete"><h1>Toutes les annonces</h1></div><p class="sous-titre">Les mots cherchés s’appliquent au titre, à la description, au quartier et à la rubrique.</p></div>
{filtres(A, [], avec_rubrique=True)}
<main class="int">{grille(A, '', '<div class="vide"><b>Pas encore d’annonce</b>Soyez le premier : la première annonce est offerte.</div>')}</main>
{pied('')}{SCRIPT_FILTRES}
<script>(function(){{var q=new URLSearchParams(location.search).get('q');var i=document.querySelector('.cherche input');if(q&&i)i.value=q;}})();</script>'''
open('recherche.html', 'w', encoding='utf-8').write(squelette('Recherche — Jaayal ma', 'Recherchez parmi toutes les annonces Jaayal ma.', rech, '', 'recherche.html'))

# ── Les six rubriques : exactement la même page ───────────────────────────────────────────────
os.makedirs('r', exist_ok=True); os.makedirs('a', exist_ok=True)
for k, (n, d, s) in FEN.items():
    items = [a for a in A if a['fenetre'] == k]
    vide = f'<div class="vide"><b>Pas encore d’annonce dans {E(n)}</b>Soyez le premier : <a href="../deposer.html">déposez ici</a> ou dites « Bia, jaayal ma ». Pendant le lancement, la première annonce de 7 jours est offerte.</div>'
    corps = f'''{entete('../', k)}
<div class="int"><p class="fil"><a href="../index.html">Jaayal ma</a> › <span>{E(n)}</span></p>
<div class="tete"><h1>{E(n)}</h1></div><p class="sous-titre">{E(d)} Classement : Premium, Prioritaire, puis par date.</p></div>
{filtres(items, s)}
<main class="int">{grille(items, '../', vide)}
<div class="appel"><div><b>Vous vendez dans {E(n)} ?</b><span>7 jours en ligne pour 1 000 F, validée par KHALAM, lue par Bia.</span></div><a class="bdeposer" href="../deposer.html">+ Déposer une annonce</a></div></main>
{pied('../')}{SCRIPT_FILTRES}'''
    open(f'r/{k}.html', 'w', encoding='utf-8').write(squelette(f'{n} — Jaayal ma', f'{n} à Dakar : {d} Annonces validées par KHALAM.', corps, '../', f'r/{k}.html'))

# ── Pages annonces ────────────────────────────────────────────────────────────────────────────
SECURITE = '''<div class="securite"><b>Conseils de sécurité</b><ul><li>Rencontrez le vendeur en personne, dans un lieu public, avant tout paiement.</li><li>Vérifiez le bien (papiers, état, fonctionnement) avant de payer.</li><li>Ne versez jamais d’acompte à distance ; un paiement Wave se vérifie dans l’application, pas par SMS.</li><li>Un doute ? Écrivez à KHALAM depuis Bia Xarit.</li></ul></div>'''
for a in A:
    fn, _, _ = FEN[a['fenetre']]; niv = NIV.get(a['niveau'], '')
    photos = a['photos']
    galerie = (f'<img class="grande" id="grande" src="../img/{photos[0]}" alt="{E(a["titre"])}">' if photos else '<div class="nophoto">Pas de photo</div>')
    vign = ('<div class="vignettes">' + ''.join(f'<img src="../img/{p_}" alt="photo {i_+1}" data-i="{i_}"{" aria-current=true" if i_==0 else ""}>' for i_, p_ in enumerate(photos)) + '</div>') if len(photos) > 1 else ''
    etiq = (f'<span class="etiq {a["niveau"]}">{niv}</span>' if niv else '') + f'<span class="etiq offre">{TYPE.get(a["type"],"")}</span>'
    lignes = [("Type", TYPE.get(a['type'], ''))] + ([("État", E(a['etat']))] if a['etat'] else []) + [(E(k_), E(str(v_))) for k_, v_ in a['details'].items() if v_] + [ ("Rubrique", f'<a href="../r/{a["fenetre"]}.html">{E(fn)}</a>'), ("Sous-rubrique", E(a['sous'])), ("Quartier", E(a['quartier']))]
    if a['surface']: lignes.append(("Surface", E(str(a['surface']))))
    lignes += [("Vendeur", 'Professionnel' if a['pro'] else 'Particulier'), ("Publiée le", dmy(a['depuis'])), ("En ligne jusqu’au", dmy(a['expire'])), ("Référence", a['id'])]
    caract = ''.join(f'<tr><th>{t}</th><td>{v}</td></tr>' for t, v in lignes if v)
    initiale = E((a.get('vendeur') or 'K')[0].upper())
    similaires = [b for b in A if b['id'] != a['id'] and b['fenetre'] == a['fenetre'] and b['sous'] == a['sous']][:3]
    if len(similaires) < 3: similaires += [b for b in A if b['id'] != a['id'] and b['fenetre'] == a['fenetre'] and b not in similaires][:3-len(similaires)]
    partage = f"https://wa.me/?text={html.escape(a['titre'])}%20-%20{F(a['prix']).replace(' ','%20')}%20-%20{a['page']}"
    corps = f'''{entete('../', a['fenetre'])}
<div class="int"><p class="fil"><a href="../index.html">Jaayal ma</a> › <a href="../r/{a['fenetre']}.html">{E(fn)}</a>{(' › <a href="../r/'+a['fenetre']+'.html#'+slug(a['sous'])+'">'+E(a['sous'])+'</a>') if a['sous'] else ''}</p></div>
<main class="int fiche">
<article>
<div class="galerie">{galerie}</div>{vign}
<h1>{E(a['titre'])}</h1>{f'<div class="wo">{E(a["titre_wo"])}</div>' if a['titre_wo'] and a['titre_wo']!=a['titre'] else ''}
<div class="ligne-prix"><div class="prix">{F(a['prix'])}<small> {E(a['unite'])}</small></div>{etiq}</div>
<div class="repere"><span>📍 <b>{E(a['quartier'])}</b>, Dakar</span><span>Publiée le {dmy(a['depuis'])}</span><span>par <b>{E(a['vendeur'] or 'Vendeur')}</b></span><span>Réf. {a['id']}</span></div>
<h2 class="bloc">Description</h2><p class="desc">{E(a['desc'])}</p>
<h2 class="bloc">Caractéristiques</h2><table class="caract">{caract}</table>
{f'<p class="cite">★ Annonce Premium : Bia la cite en premier à ceux qui cherchent dans {E(fn)} à {E(a["quartier"])}.</p>' if a['niveau']=='premium' else ''}
</article>
<aside class="lateral">
<div class="vendeur"><div class="qui"><div class="av">{initiale}</div><div><b>{E(a.get('vendeur') or 'Vendeur')}</b><span>{'Professionnel' if a['pro'] else 'Particulier'} · {E(a['quartier'])}</span></div></div>
<a class="bwa" href="{a['whatsapp']}">{WA_SVG} Écrire sur WhatsApp</a>
<a class="btel" href="tel:{a['tel'].replace(' ','')}">📞 {E(a['tel'])}</a>
<p class="verif"><i>✓</i> Numéro vérifié · annonce relue et validée par KHALAM le {dmy(a['depuis'])}</p></div>
<div class="partage"><a href="{partage}">Partager sur WhatsApp</a><button type="button" id="copier" data-url="{a['page']}">Copier le lien</button></div>
<a class="signaler" href="https://khalam.app/bia">⚑ Signaler cette annonce à KHALAM</a>
{SECURITE}
</aside>
{f'<section class="similaires"><h2 class="sec">Annonces similaires <a href="../r/{a["fenetre"]}.html">Toute la rubrique →</a></h2><div class="grille">{"".join(carte(b, "../") for b in similaires)}</div></section>' if similaires else ''}
</main>
{pied('../')}
<script>(function(){{var g=document.getElementById('grande'),v=document.querySelectorAll('.vignettes img');v.forEach(function(im){{im.addEventListener('click',function(){{g.src=im.src;v.forEach(function(x){{x.removeAttribute('aria-current')}});im.setAttribute('aria-current','true');}});}});
var c=document.getElementById('copier');if(c)c.addEventListener('click',function(){{var u=c.dataset.url;function ok(){{c.textContent='Lien copié ✓';setTimeout(function(){{c.textContent='Copier le lien'}},1800)}}
if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(u).then(ok,function(){{prompt('Copiez le lien :',u)}})}}else{{prompt('Copiez le lien :',u)}}}});}})();</script>'''
    desc = f"{a['titre']} — {F(a['prix'])}{a['unite']}, {a['quartier']}. {a['desc'][:120]}"
    open(f"a/{a['id']}.html", 'w', encoding='utf-8').write(squelette(f"{a['titre']} — {F(a['prix'])}{a['unite']} à {a['quartier']} | Jaayal ma", desc, corps, '../', f"a/{a['id']}.html"))

# Retirer les anciennes pages d'annonces qui ne figurent plus dans la source.
pages_attendues = {f"{a['id']}.html" for a in A}
for nom in os.listdir('a'):
    chemin = os.path.join('a', nom)
    if nom.endswith('.html') and nom not in pages_attendues and os.path.isfile(chemin):
        os.remove(chemin)

# ── annonces.json : ce que Bia lit (fenêtres documentées) ─────────────────────────────────────
D['annonces'] = A
D['fenetres'] = {k: {'nom': n, 'description': d, 'sous_rubriques': s} for k, n, d, s in FENETRES}
D['genere'] = datetime.date.today().isoformat()
json.dump(D, open('annonces.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(FEN), 'rubriques,', len(A), 'annonces')
