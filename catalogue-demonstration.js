/* KHALAM · CATALOGUE D'EXEMPLES · 2026-11-22
   Présentation uniquement. Aucune annonce réelle, aucun contact, aucun prix.
   Ne modifie pas annonces.json ni les relais BIA/WhatsApp.
   Retirable en supprimant cette inclusion <script> des pages concernées. */
(function(){
"use strict";
var exemples={"immobilier":[["Location de studio meublé","Location","🏠","Exemple de fiche : un studio lumineux, une kitchenette et une salle d’eau indépendante.","#cde8ff"],["Maison familiale avec cour","Vente","🏡","Exemple de présentation : maison avec cour intérieure et plusieurs pièces à visiter.","#dcf3df"],["Terrain constructible","Vente","🌳","Exemple illustratif : terrain à évaluer, dimensions et documents à confirmer.","#e6e4c8"],["Appartement avec balcon","Location","🏢","Exemple de fiche immobilière : appartement, balcon et description des commodités.","#e3dffd"],["Local commercial","Location","🏬","Exemple de publication : boutique ou bureau, superficie et conditions à préciser.","#fbe8d1"],["Chambre à louer","Location","🚪","Exemple de présentation d’une chambre avec accès et équipements décrits.","#f8dfd9"]],"vehicules":[["Voiture citadine","Voitures","🚗","Exemple de fiche auto : marque, année, kilométrage et état mécanique à renseigner.","#dce9ff"],["Moto urbaine","Motos & scooters","🏍️","Exemple de présentation d’une moto : cylindrée, documents et entretien à vérifier.","#ffe1d0"],["Scooter de déplacement","Motos & scooters","🛵","Exemple de fiche : scooter destiné aux trajets quotidiens et caractéristiques à compléter.","#d3f1f0"],["Location de véhicule","Location de voitures","🚙","Exemple de service : modalités, assurance et disponibilité à préciser.","#e0e9d3"],["Pneus et jantes","Pièces & pneus","🛞","Exemple de publication de pièces automobiles : dimensions et compatibilité.","#e7e7ed"],["Pièce de rechange automobile","Pièces & pneus","🔧","Exemple : état, référence et compatibilité du modèle à vérifier.","#dbe3f7"]],"electromenager":[["Téléviseur écran plat","Télé, téléphones & ordinateurs","📺","Exemple de fiche TV : diagonale, résolution, accessoires et fonctionnement à préciser.","#d8e5ff"],["Vidéoprojecteur familial","Télé, téléphones & ordinateurs","📽️","Exemple illustratif : luminosité, connectiques et projection à renseigner.","#e3ddff"],["TV Box multimédia","Télé, téléphones & ordinateurs","📦","Exemple de publication TV Box : système, stockage et accessoires.","#d9f3f3"],["Réfrigérateur deux portes","Électroménager","🧊","Exemple de fiche : capacité, dimensions et état du réfrigérateur.","#d7efff"],["Canapé de salon","Meubles & décoration","🛋️","Exemple de présentation de mobilier : dimensions, matière et coloris.","#f5e3db"],["Ustensiles de cuisine","Cuisine & ustensiles","🍳","Exemple de lot de cuisine : composition et état à détailler.","#fff0cc"]],"mode":[["Grand boubou brodé","Vide-dressing","👘","Exemple de présentation textile : taille, tissu, broderies et état à préciser.","#f7d5e6"],["Bazin riche","Tissus & bazin","🧵","Exemple de fiche tissu : métrage, teinte et qualité à décrire.","#d9d6fa"],["Montre classique","Bijoux & montres","⌚","Exemple : marque, matière et état de la montre à vérifier.","#f2e5c7"],["Sac à main","Vide-dressing","👜","Exemple de publication d’un sac : dimensions, matière et état.","#fce5d5"],["Chaussures de ville","Vide-dressing","👞","Exemple : pointure et détails de l’article à renseigner.","#e0d9d2"],["Accessoires de coiffure","Beauté & mèches","💇🏽‍♀️","Exemple de fiche beauté : composition et caractéristiques à confirmer.","#f1dcf1"]],"animaux":[["Mouton pour élevage","Moutons","🐑","Exemple d’annonce : âge, santé et provenance de l’animal à renseigner.","#e8f3d4"],["Chèvre d’élevage","Bœufs & chèvres","🐐","Exemple de fiche : âge, alimentation et état sanitaire à documenter.","#f6e8c9"],["Bœuf d’élevage","Bœufs & chèvres","🐂","Exemple de présentation : poids indicatif et documents sanitaires à vérifier.","#e0e3d8"],["Poules et volailles","Volailles","🐓","Exemple de fiche volailles : race, âge et conditions d’élevage.","#fff1cf"],["Chat de compagnie","Chiens & chats","🐈","Exemple éducatif : état de santé, vaccination et conditions d’adoption.","#f9e4da"],["Chien de compagnie","Chiens & chats","🐕","Exemple de fiche d’adoption responsable : identification et suivi vétérinaire.","#d8e6fa"]],"services":[["Réparation électroménager","Services","🧰","Exemple de service : zone d’intervention et qualifications à préciser.","#dfedff"],["Cours de soutien scolaire","Services","📚","Exemple de fiche : niveau, matières et modalités des séances.","#e4e1ff"],["Offre de stage","Emplois","💼","Exemple illustratif d’une annonce d’emploi avec missions et conditions à compléter.","#e4f2dc"],["Location de chaises pour événement","Événements (chaises, bâches, sono)","🪑","Exemple de prestation : quantités et conditions de livraison à préciser.","#f7e6d5"],["Vélo et accessoires","Sport & loisirs","🚲","Exemple d’équipement sportif : taille, état et accessoires à décrire.","#dff4e6"],["Matériel pour chantier","Matériel pro & BTP","🧱","Exemple de fiche professionnelle : caractéristiques et état du matériel.","#f0e7db"]]};
var path=location.pathname.toLowerCase();
var fenetre=path.match(/\/r\/([^/]+)\.html$/);
var scope=fenetre?fenetre[1]:/\/recherche\.html$/.test(path)?"toutes":null;
if(!scope||(!exemples[scope]&&scope!=="toutes"))return;
var grille=document.getElementById("grille");if(!grille)return;
if(grille.querySelector(".khalam-demo"))return;
var style=document.createElement("style");
style.textContent=".khalam-demo{outline:1px solid #bfcbd7!important;border-style:dashed!important;background:#f8fafc!important}.khalam-demo .visuel{min-height:150px;aspect-ratio:4/3;display:grid;place-items:center;overflow:hidden}.khalam-demo .illustration{font-size:clamp(56px,7vw,84px);filter:drop-shadow(0 4px 7px #1f314b29);line-height:1}.khalam-demo .demo-badge{position:absolute;top:8px;left:8px;z-index:2;padding:5px 8px;border-radius:7px;background:#123a5e;color:white;font-size:10px;font-weight:900;letter-spacing:.05em}.khalam-demo .type{font-size:10px}.khalam-demo .prix{font-size:14px;color:#265582}.khalam-demo .wo{font-size:12px;line-height:1.4;color:#53687c}.khalam-demo .meta{font-size:11px}.khalam-demo-notice{margin:15px 0 20px;padding:13px 17px;background:#e8f3ff;border-left:4px solid #2975b3;border-radius:9px;font-size:13px;line-height:1.55;color:#1d425e}.khalam-demo-note-link{font-weight:800;text-decoration:underline}.khalam-demo[hidden]{display:none!important}";
document.head.appendChild(style);
function el(tag,cls,txt){var x=document.createElement(tag);if(cls)x.className=cls;if(txt!==undefined)x.textContent=txt;return x}
var all=[];
Object.keys(exemples).forEach(function(k){exemples[k].forEach(function(row,i){all.push({rubrique:k,titre:row[0],sous:row[1],icone:row[2],description:row[3],couleur:row[4],numero:i})})});
var present=scope==="toutes"?all:all.filter(function(x){return x.rubrique===scope});
present.forEach(function(x){
var card=el("a","carte normale khalam-demo");
card.href=path.indexOf("/r/")>=0?"../deposer.html":"deposer.html";
card.setAttribute("aria-label","Démonstration, produit non disponible : "+x.titre+". Déposer une véritable annonce");
card.dataset.q="";card.dataset.s=x.sous;card.dataset.f=x.rubrique;card.dataset.p="0";card.dataset.d="2026-11-22";card.dataset.r="9";
card.dataset.t=(x.titre+" "+x.description+" "+x.sous+" démonstration").toLowerCase();
var vis=el("div","visuel");vis.style.background="linear-gradient(145deg,"+x.couleur+",#ffffff)";
vis.appendChild(el("span","illustration",x.icone));
vis.appendChild(el("span","demo-badge","EXEMPLE · NON DISPONIBLE"));
vis.appendChild(el("span","type","Démo uniquement"));
var corps=el("div","corps");
corps.appendChild(el("div","prix","Annonce fictive · sans prix"));
corps.appendChild(el("div","titre",x.titre));
corps.appendChild(el("div","wo",x.description));
var attrs=el("div","attrs");attrs.appendChild(el("span","",x.sous));corps.appendChild(attrs);
var meta=el("div","meta");meta.appendChild(el("span","","Illustration KHALAM"));meta.appendChild(el("span","","Déposer une vraie annonce"));corps.appendChild(meta);
card.appendChild(vis);card.appendChild(corps);grille.appendChild(card);
});
var empty=grille.querySelectorAll(".vide:not(#vide-filtre)");
[].forEach.call(empty,function(node){node.hidden=true});
var notice=el("aside","khalam-demo-notice");
notice.setAttribute("role","note");
notice.textContent="CATALOGUE DE DÉMONSTRATION — Ces "+present.length+" fiches sont des exemples fictifs et non disponibles : aucune offre réelle, aucun vendeur, aucun prix et aucun contact. Elles servent uniquement à montrer la présentation des rubriques avant l’arrivée d’annonces autorisées. ";
var link=el("a","khalam-demo-note-link","Publier une vraie annonce");
link.href=path.indexOf("/r/")>=0?"../deposer.html":"deposer.html";
notice.appendChild(link);
grille.parentNode.insertBefore(notice,grille);
})();
