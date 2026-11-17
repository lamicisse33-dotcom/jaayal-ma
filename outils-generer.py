import json, html, re, datetime, os
D=json.load(open('annonces.json')); A=D['annonces']
old=open('index.html',encoding='utf-8').read()
CSS=old[old.index('<style>'):old.index('</style>')+8]
if '.familles' not in CSS: CSS=CSS.replace('</style>','''
.familles{display:flex;flex-direction:column;gap:26px;margin-top:6px}
.famille h2{font-family:var(--display);font-size:20px;margin:0 0 10px;letter-spacing:-.01em;display:flex;align-items:baseline;gap:10px}
.famille h2 small{font:500 12.5px var(--texte);color:var(--doux);letter-spacing:.04em;text-transform:uppercase}
.fenetres{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.fenetre{background:var(--carte);border:1px solid var(--ligne);border-radius:16px;padding:14px 16px 12px;text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px;min-width:0;position:relative}
.fenetre b{font-family:var(--display);font-size:16.5px;line-height:1.2}
.fenetre span{font-size:13px;color:var(--doux);line-height:1.45}
.fenetre .n{margin-top:auto;padding-top:8px;font-size:12.5px;color:var(--marine);font-weight:600;display:flex;justify-content:space-between;align-items:center}
.fenetre .n em{font-style:normal;color:var(--doux);font-weight:500}
.fenetre .n i{font-style:normal}
.fenetre .apercu{display:flex;gap:6px;margin-top:4px}
.fenetre .apercu img{width:52px;height:40px;object-fit:cover;border-radius:7px;border:1px solid var(--ligne)}
@media (prefers-reduced-motion:no-preference){.fenetre{transition:transform .15s}.fenetre:hover{transform:translateY(-2px)}}
.fil{font-size:13px;color:var(--doux);margin:0 0 6px}.fil a{text-decoration:none}
.vide{background:var(--carte);border:1px dashed var(--ligne);border-radius:14px;padding:26px 18px;text-align:center;color:var(--doux)}
.vide b{display:block;color:var(--fg);font-family:var(--display);font-size:17px;margin-bottom:4px}
.sousliste{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.sousliste span{font-size:12.5px;border:1px solid var(--ligne);background:var(--carte);border-radius:999px;padding:4px 10px;color:var(--doux)}
</style>''')
HEAD='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap">'
def F(n): return f"{n:,}".replace(","," ")+" F"
NIV={"premium":("Premium","Bia la cite en premier"),"prioritaire":("Prioritaire",""),"normale":("","")}
TYPE={"vente":"À vendre","location":"À louer"}
# ── Les fenêtres, famille par famille ─────────────────────────────────────
FAM=[
 ("Six pages",[
  ("immobilier","Immobilier","Vente et location : maisons, appartements, chambres, terrains, commerces et locaux.",["Vente","Location"]),
  ("vehicules","Véhicules","Voitures, motos et scooters, location de voitures, pièces et pneus.",["Voitures","Motos & scooters","Location de voitures","Pièces & pneus"]),
  ("electromenager","Électroménager & maison","Frigos, machines, ventilateurs, télés, téléphones, ordinateurs, meubles, cuisine.",["Électroménager","Télé, téléphones & ordinateurs","Meubles & décoration","Cuisine & ustensiles"]),
  ("mode","Mode & bijoux","Vide-dressing (habits), bijoux et montres, tissus et bazin, beauté.",["Vide-dressing","Bijoux & montres","Tissus & bazin","Beauté & mèches"]),
  ("animaux","Animaux","Moutons de Tabaski, bœufs et chèvres, volailles, chiens et chats.",["Moutons","Bœufs & chèvres","Volailles","Chiens & chats"]),
  ("services","Services & divers","Services, emplois, événements, sport et loisirs, bébé et enfants, matériel pro.",["Services","Emplois","Événements (chaises, bâches, sono)","Sport & loisirs","Bébé & enfants","Matériel pro & BTP"]),
 ]),
]
FEN={k:(n,d,s) for _,l in FAM for k,n,d,s in l}
# répartition des annonces fictives dans les fenêtres
MAP={'villa-almadies-4ch':'immobilier','appart-mermoz-3p':'immobilier','chambre-pikine-rue10':'immobilier','maison-keur-massar':'immobilier','terrain-rufisque-300':'immobilier','boutique-sacre-coeur':'immobilier','restaurant-ngor-cession':'immobilier','tucson-2021-dakar':'vehicules','corolla-2018-pikine':'vehicules','peugeot-308-ouakam':'vehicules','tv-samsung-55':'electromenager','ventilateur-binatone':'electromenager','frigo-hisense-2-portes':'electromenager','grand-boubou-bazin':'mode','montre-homme-cuir':'mode','collier-or-18k':'mode'}
PARTIE={'villa-almadies-4ch':'Vente','maison-keur-massar':'Vente','terrain-rufisque-300':'Vente','restaurant-ngor-cession':'Vente','appart-mermoz-3p':'Location','chambre-pikine-rue10':'Location','boutique-sacre-coeur':'Location','tucson-2021-dakar':'Voitures','corolla-2018-pikine':'Voitures','peugeot-308-ouakam':'Voitures','tv-samsung-55':'Télé, téléphones & ordinateurs','ventilateur-binatone':'Électroménager','frigo-hisense-2-portes':'Électroménager','grand-boubou-bazin':'Vide-dressing','montre-homme-cuir':'Bijoux & montres','collier-or-18k':'Bijoux & montres'}
for a in A: a['fenetre']=MAP[a['id']]; a['sous']=PARTIE[a['id']]
def bande(prefix=''):
    return f'''<div class="maquette">Maquette — annonces, noms et numéros fictifs, pour voir l’effet. Rien ici n’est réel.</div>
<header class="bande"><div class="int"><a class="marque" href="{prefix}index.html"><b>Jaayal ma</b><span>par KHALAM</span></a><nav><a href="{prefix}index.html#fenetres">Rubriques</a><a href="{prefix}index.html#tarifs">Tarifs</a><a href="{prefix}index.html#comment">Déposer</a><a href="https://khalam.app/bia">Bia Xarit</a></nav></div></header>'''
def carte(a,prefix=''):
    niv,cite=NIV[a['niveau']]; badge=f'<span class="badge {a["niveau"]}">{niv}</span>' if niv else ''
    return f'''<a class="carte {a['niveau']}" href="{prefix}a/{a['id']}.html" data-q="{html.escape(a['quartier'])}">
<img src="{prefix}img/{a['photos'][0]}" alt="{html.escape(a['titre'])}" loading="lazy">{badge}<span class="type">{TYPE[a['type']]}</span>
<div class="corps"><div class="prix">{F(a['prix'])} <small>{a['unite']}</small></div><div class="titre">{html.escape(a['titre'])}</div><div class="wo">{html.escape(a['titre_wo'])}</div>
{f'<div class="cite">★ {cite}</div>' if cite else ''}
<div class="meta"><span><b>{html.escape(a['quartier'])}</b>{(' · '+html.escape(a['sous'])) if a.get('sous') else ''}</span><span>{'Pro' if a['pro'] else 'Particulier'} · expire le {a['expire'][8:10]}/{a['expire'][5:7]}</span></div></div></a>'''
def fenetre_tuile(k):
    n,d,s=FEN[k]; items=[a for a in A if a['fenetre']==k]
    apercu=''.join(f'<img src="img/{a["photos"][0]}" alt="">' for a in items[:3])
    compte=f'<i>{len(items)} annonce{"s" if len(items)>1 else ""}</i>' if items else '<em>Bientôt vos annonces</em>'
    return f'<a class="fenetre" href="r/{k}.html"><b>{n}</b><span>{d}</span>{f"<div class=apercu>{apercu}</div>" if apercu else ""}<div class="n">{compte}<i>→</i></div></a>'
TARIFS='''<section class="tarifs" id="tarifs"><h2>Tarifs</h2><p>Vous payez par jour d’affichage, à partir de 3 jours. Plus le niveau est haut, plus l’annonce est vue.</p>
<table><thead><tr><th>Niveau</th><th>Par jour</th><th>7 jours</th><th>30 jours</th></tr></thead><tbody>
<tr class="premium"><td>Premium — tout en haut de sa rubrique, et Bia la cite en premier à la voix</td><td>1 000 F</td><td>7 000 F</td><td>30 000 F</td></tr>
<tr class="prioritaire"><td>Prioritaire — au-dessus des annonces normales</td><td>500 F</td><td>3 500 F</td><td>15 000 F</td></tr>
<tr><td>Normale — dans la liste, par date</td><td>300 F</td><td>2 000 F</td><td>9 000 F</td></tr></tbody></table>
<p class="note">Professionnels (agences, courtiers, boutiques, vendeurs de véhicules) : forfait 15 000 F par mois, annonces normales illimitées, Prioritaire et Premium à moitié prix. Paiement par Wave ou Orange Money. Pendant le lancement, la première annonce de 7 jours est offerte.</p></section>'''
COMMENT='''<section class="comment" id="comment"><h2>Comment ça marche</h2>
<div><b>1. Vous parlez</b><p>Dans Bia Xarit, dites « Bia, jaayal ma ». Elle vous demande quoi, où, combien, et prend les photos avec vous. En wolof ou en français.</p></div>
<div><b>2. KHALAM valide</b><p>Rien n’est publié sans vérification : votre numéro est connu, votre annonce est relue. C’est ce qui fait la différence avec un groupe WhatsApp.</p></div>
<div><b>3. Elle est en ligne</b><p>Votre annonce a sa page ici, dans sa rubrique, partageable sur WhatsApp, et Bia la propose à tous ceux qui cherchent dans votre quartier.</p></div>
<div><b>4. On vous contacte</b><p>Les acheteurs vous écrivent directement sur WhatsApp. Vous prolongez ou retirez l’annonce à la voix, quand vous voulez.</p></div></section>'''
FOOT='<footer>Jaayal ma est un service de <a href="https://khalam.app">KHALAM</a>, Dakar. Les annonces sont publiées sous la responsabilité de leurs auteurs après validation par KHALAM. · <a href="https://khalam.app/bia">Bia Xarit</a> · <a href="{p}annonces.json">annonces.json</a> (ce que Bia lit)</footer>'
index=f'''<title>Jaayal ma</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Jaayal ma — les annonces de Dakar validées par KHALAM, rubrique par rubrique : maisons, voitures, électroménager, vide-dressing, bijoux, moutons, services… Dites « Bia, jaayal ma ».">
{HEAD}{CSS}
{bande()}
<section class="hero"><h1>Tout se vend à Dakar. Ici, <em>chaque chose a sa page</em>.</h1><p>Une maison, une voiture, un frigo, un boubou, un collier, un mouton : six pages seulement, chacune avec ses rubriques : tout l’immobilier sur une page, vente et location ; tous les animaux sur une autre. Chaque annonce est relue par KHALAM avant d’être publiée, et Bia Xarit la propose à la voix à ceux qui cherchent.</p>
<div class="dire"><i>B</i>Pour déposer : dites <b>« Bia, jaayal ma »</b></div></section>
<main id="fenetres"><div class="familles">
{''.join(f'<section class="famille"><div class="fenetres">{"".join(fenetre_tuile(k) for k,_,_,_ in l)}</div></section>' for fam,l in FAM)}
</div>
{TARIFS}{COMMENT}</main>
{FOOT.format(p='')}'''
open('index.html','w',encoding='utf-8').write(index)
os.makedirs('r',exist_ok=True)
def SK(t,d,c): return '<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<title>'+t+'</title>\n<meta name="description" content="'+d+'">\n'+HEAD+CSS+'\n</head><body>'+c+'\n</body></html>'
for k,(n,d,s) in FEN.items():
    items=[a for a in A if a['fenetre']==k]; quartiers=sorted(set(a['quartier'] for a in items))
    corps=f'''{bande('../')}
<section class="hero"><p class="fil"><a href="../index.html">Jaayal ma</a> › {n}</p><h1>{n}</h1><p>{d}</p>
<div class="sousliste">{''.join(f'<a href="#{re.sub(r"[^a-z0-9]+","-",x.lower())}" style="text-decoration:none"><span>{x}</span></a>' for x in s)}</div></section>
<div class="filtres"><div class="int"><span class="compte" style="margin:0">{len(items)} annonce{'s' if len(items)>1 else ''} · dans chaque partie : Premium, Prioritaire, puis par date</span>
<select id="quartier" aria-label="Quartier"><option value="">Tous les quartiers</option>{''.join(f'<option>{html.escape(q)}</option>' for q in quartiers)}</select></div></div>
<main>{''.join(f'<section class="famille" id="{re.sub(r"[^a-z0-9]+","-",p.lower())}"><h2>{p} <small>{len([a for a in items if a["sous"]==p])} annonce{"s" if len([a for a in items if a["sous"]==p])>1 else ""}</small></h2><div class="grille">{"".join(carte(a,"../") for a in items if a["sous"]==p)}</div></section>' for p in s if any(a["sous"]==p for a in items)) if items else f'<div class="vide"><b>Pas encore d’annonce dans {n}</b>Soyez le premier : dites « Bia, jaayal ma » et choisissez cette rubrique. Pendant le lancement, la première annonce de 7 jours est offerte.</div>'}
</main>
{FOOT.format(p='../')}
<script>(function(){{var sel=document.getElementById('quartier');if(!sel)return;var cartes=document.querySelectorAll('.carte');sel.addEventListener('change',function(){{cartes.forEach(function(c){{c.hidden=!!sel.value&&c.dataset.q!==sel.value;}});}});}})();</script>'''
    open(f'r/{k}.html','w',encoding='utf-8').write(SK(html.escape(n)+' — Jaayal ma',html.escape(d),corps))
for a in A:
    niv,cite=NIV[a['niveau']]; badge=f'<span class="badge {a["niveau"]}">{niv}</span>' if niv else ''
    fn=FEN[a['fenetre']][0]
    corps=f'''{bande('../')}
<article class="fiche"><p class="fil"><a href="../index.html">Jaayal ma</a> › <a href="../r/{a['fenetre']}.html">{fn}</a></p>
<div class="photo"><img src="../img/{a['photos'][0]}" alt="{html.escape(a['titre'])}">{badge}<span class="type">{TYPE[a['type']]}</span></div>
<h1>{html.escape(a['titre'])}</h1><div class="wo">{html.escape(a['titre_wo'])}</div>
<div class="prix">{F(a['prix'])} <small>{a['unite']}</small></div>
<div class="infos"><div><span>Quartier</span><b>{html.escape(a['quartier'])}</b></div><div><span>Rubrique</span><b>{fn}{(' · '+html.escape(a['sous'])) if a.get('sous') else ''}</b></div>{f'<div><span>Surface</span><b>{a["surface"]}</b></div>' if a['surface'] else ''}<div><span>Publiée le</span><b>{a['depuis'][8:10]}/{a['depuis'][5:7]}/{a['depuis'][:4]}</b></div><div><span>Expire le</span><b>{a['expire'][8:10]}/{a['expire'][5:7]}/{a['expire'][:4]}</b></div></div>
<p class="desc">{html.escape(a['desc'])}</p>
<div class="contact"><a class="bwa" href="{a['whatsapp']}">Écrire sur WhatsApp</a><span class="tel">{a['tel']}</span></div>
<p class="verif"><i>✓</i> Annonce de {html.escape(a['vendeur'])}{' (professionnel)' if a['pro'] else ''} · numéro vérifié · validée par KHALAM</p>
{f'<p class="cite">★ {cite} à ceux qui cherchent dans {fn} à {html.escape(a["quartier"])}.</p>' if cite else ''}
</article>
{FOOT.format(p='../')}'''
    open(f"a/{a['id']}.html",'w',encoding='utf-8').write(SK(html.escape(a['titre']),html.escape(a['titre'])+' — '+F(a['prix'])+a['unite']+', '+html.escape(a['quartier'])+'. Annonce Jaayal ma validée par KHALAM.',corps))
D['fenetres']={k:{'nom':n,'description':d,'sous_rubriques':s,'famille':fam} for fam,l in FAM for k,n,d,s in l}
json.dump(D,open('annonces.json','w'),ensure_ascii=False,indent=1)
print(len(FEN),'fenêtres')
