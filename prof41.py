import os
from flask import Flask, request, render_template

app = Flask(__name__)

PROFESSIONS = {
    "militaire": "militaire.txt",
    "fisc": "fisc.txt",
    "cadastre": "cadastre.txt",
    "police": "police.txt",
    "notaire": "notaire.txt"
}

def lire_texte(nom_fichier):
    """Lit le contenu d'un fichier texte et supprime les gros titres inutiles."""
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
            # Supprimer les lignes en majuscules (souvent des titres inutiles)
            lignes = contenu.splitlines()
            lignes_filtrees = [ligne for ligne in lignes if not ligne.isupper()]
            return "\n".join(lignes_filtrees)
    except FileNotFoundError:
        return "Information non disponible."

@app.route("/")
def recherche():
    return render_template("index.html", professions=PROFESSIONS.keys())

@app.route("/profession", methods=["POST"])
def profession():
    profession = request.form.get("profession")
    nom_fichier = PROFESSIONS.get(profession)
    if nom_fichier:
        message = lire_texte(nom_fichier)
    else:
        message = f"Aucune information disponible pour : {profession}."
    return render_template("index.html", message=message, professions=PROFESSIONS.keys())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
