import os
from flask import Flask, request, render_template

app = Flask(__name__)

# 🔹 Rubriques générales
RUBRIQUES = {
    
    "enigme": "enigme.txt",
    "fisc": "fisc.txt",
    "cadastre": "cadastre.txt",
    "police": "police.txt",
    "region": "region.txt",
    "notaire": "notaire.txt",
    "Alsace": "Alsace.txt"
}

# 🔹 Professions spécifiques
PROFESSIONS = {
    "chanvrier": "chanvrier.txt",
    "chapelier": "chapelier.txt",
    "douanier": "douanier.txt",
    "fonctionnaire": "fonctionnaire.txt",
    "soldat": "soldat.txt",
    "militaire": "militaire.txt"
}
# 🧠 Analyse des règles
    if prof == "douanier" and naissance and 1760 < naissance < 1810:
        msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

    if "alsace" in lieu and naissance and 1870 < naissance < 1918:
        msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : consulter ANOM ou archives allemandes.")

    if prof == "orfèvre":
        msg.append("💎 Orfèvre : consulter les registres de poinçons.")

    if militaire :
        msg.append("🎖️ Militaire blessé/officier : consulter les registres militaires.")

    if celibataire and etatcivil:
        msg.append("📜 Célibataire avec acte complet : voir actes notariés et mentions marginales.")











# 🔹 Rubriques critère
CARACTERISTIQUE = {
    "z": "z.txt",
    "banque": "banque.txt"
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

        if rubrique in RUBRIQUES:
            message += f"📁 Rubrique sélectionnée : {rubrique.capitalize()}\n"
            message += lire_texte(RUBRIQUES[rubrique]) + "\n"

        if profession in PROFESSIONS:
            message += f"\n👤 Profession sélectionnée : {profession.capitalize()}\n"
            message += lire_texte(PROFESSIONS[profession]) + "\n"

        if caracteristique in CARACTERISTIQUE:
            message += f"\n🔍 Caractéristique sélectionnée : {caracteristique.capitalize()}\n"
            message += lire_texte(CARACTERISTIQUE[caracteristique]) + "\n"

    return render_template("index.html",
                           message=message,
                           rubriques=RUBRIQUES.keys(),
                           professions=PROFESSIONS.keys(),
                           caracteristique=CARACTERISTIQUE.keys())

# 🔹 Lancement du serveur
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

