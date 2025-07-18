import os
from flask import Flask, request, render_template

app = Flask(__name__)

# 🔹 Rubriques générales (liées à des fichiers texte)
PROFESSIONS = {
    "militaire": "militaire.txt",
    "fisc": "fisc.txt",
    "cadastre": "cadastre.txt",
    "police": "police.txt",
    "notaire": "notaire.txt"
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
        profession = request.form.get("profession")
        if profession in PROFESSIONS:
            message = lire_texte(PROFESSIONS[profession])

    return render_template("index.html",
                           message=message,
                           professions=PROFESSIONS.keys())

# 🔹 Lancement du serveur
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
