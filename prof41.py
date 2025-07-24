import os
from flask import Flask, request, render_template

app = Flask(__name__)

# 🔹 Rubriques générales
RUBRIQUES = {
    "enigme": "enigme.txt",
    "introduction": "introduction.txt", 
    "recrutement": "recrutement.txt",
    "archives fiscales": "archives fiscales.txt",
    "cadastre": "cadastre.txt",
    "police": "police.txt",
    "region": "region.txt",
    "archives notariales": "archives notariales.txt",
    "commune": "commune.txt", 
    "archives banquaires" : "archives banquaires.txt",
    "archives hypothequaires: "archives hypothequaires.txt,
    "archives nobilieres" : "archives nobilieres".txt",
    "objets de famille" : "objets de familles".txt",
    "archives hospitalieres" : "archives hospitalieres".txt",
    "archives de l'enregistrement: "archivres de l'enregistrement.txt",
    "archives administratives": "archives administratives.txt", 
    "archives scolaires": "archives scolaires.txt",
    "archives judiciaires": "archives judiciaires", 
    "archives religieuses": "archives religieuses.txt",
    "archives des sepultures": "archives des sepultures.txt", 
    "Alsace-Lorraine": "Alsace-Lorraine.txt",
    "archives de l'Etat Civil": "archives de l'Etat Civil.txt",
    "Archives à l etranger": "Archives à l'etranger.txt",
    "cadendrier revolutionnaire": "calendrier revolutionnaire.txt", 
    "sites généalogiques": "sites genealogiques.txt",
    "idee de recherches": "idees de recherches.txt" 
}

# 🔹 Professions spécifiques
PROFESSIONS = {
    "chanvrier": "chanvrier.txt",
    "chapelier": "chapelier.txt",
    "douanier": "douanier.txt",
    "fonctionnaire": "fonctionnaire.txt",
    "soldat": "soldat.txt",
    "militaire": "militaire.txt",
    "pape": "pape.txt",
    "religieux": "religieux".txt,
    "francs-tireur": "francs-tireur.txt"
}

# 🔹 Caractéristiques critère
CARACTERISTIQUE = {
    "juif": "juif.txt",
    "catholique": "catholique.txt"
    "protestant": "juif.txt",
    "musulman": "musulman.txt",
    "religion inconnue" : "religion inconnue.txt"
}

# 🔹 Lecture et nettoyage des fichiers texte
def lire_texte(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            lignes = fichier.read().splitlines()
            lignes_filtrees = [ligne for ligne in lignes if not ligne.isupper()]
            lignes_nettoyees = lignes_filtrees[3:-2] if len(lignes_filtrees) > 5 else []
            return "\n".join(lignes_nettoyees)
    except FileNotFoundError:
        return "Information non disponible."

# 🔹 Route principale
@app.route("/", methods=["GET", "POST"])
def recherche():
    message = ""
    if request.method == "POST":
        rubrique = request.form.get("rubrique")
        profession = request.form.get("profession")
        caracteristique = request.form.get("caracteristique")
        lieu = request.form.get("lieu", "").lower()
        code_postal = request.form.get("code_postal", "").lower()

        try:
            date_min = int(request.form.get("date_min", 0))
            date_max = int(request.form.get("date_max", 0))
        except ValueError:
            date_min, date_max = 0, 0

        if rubrique in RUBRIQUES:
            message += f"📁 Rubrique sélectionnée : {rubrique.capitalize()}\n"
            message += lire_texte(RUBRIQUES[rubrique]) + "\n"

        if profession in PROFESSIONS:
            message += f"\n👤 Profession sélectionnée : {profession.capitalize()}\n"
            message += lire_texte(PROFESSIONS[profession]) + "\n"

        if caracteristique in CARACTERISTIQUE:
            message += f"\n🔍 Caractéristique sélectionnée : {caracteristique.capitalize()}\n"
            message += lire_texte(CARACTERISTIQUE[caracteristique]) + "\n"

        # 🔍 Logique conditionnelle
        if profession == "pape" and "avignon" in lieu and 1300 <= date_min <= 1400:
            message += ("\n📜 Archives religieuses : Les documents concernant les papes à Avignon entre 1300 et 1400 "
                        "se trouvent au diocèse. Voir rubrique 'religion'.\n")

        if profession == "douanier" and 1750 <= date_min <= 1810:
            message += ("\n📜 Douanes : Les dossiers de retraite des douaniers entre 1750 et 1810 sont aux Archives Nationales (cote XX 21).\n")

        if "alsace" in lieu and 1771 <= date_min <= 1918:
            message += ("\n📜 Alsace-Lorraine : Période prussienne avec législation spécifique. Voir rubrique 'alsace-loraine'.\n")

        if profession == "francs-tireur" and date_min == 1871:
            message += ("\n📜 Siège de Paris : En 1871, des bataillons civils comme 'À la feuille de houx' défendaient Paris. "
                        "Une statue existait devant l’église Saint-Ferdinand.\n")

        if profession == "soldat" and date_min >= 1650:
            message += ("\n📜 Armée : Des fiches matricules sont disponibles pour tous les régiments depuis 1650. "
                        "Voir rubrique 'militaire'.\n")

    return render_template("index.html",
                           message=message,
                           rubriques=RUBRIQUES.keys(),
                           professions=PROFESSIONS.keys(),
                           caracteristique=CARACTERISTIQUE.keys())

# 🔹 Lancement du serveur
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
