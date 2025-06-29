import os
from flask import Flask, request, render_template

app = Flask(__name__)

def lire_texte(nom_fichier):
    """Lit le contenu d'un fichier texte."""
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()
    except FileNotFoundError:
        return "Information non disponible."

@app.route("/")
def recherche():
    return render_template("index.html")

@app.route("/profession", methods=["GET", "POST"])
def profession():
    message = ""
    if request.method == "POST":
        profession = request.form.get("profession").lower()
        if profession == "militaire":
            message = f"cette rubrique concerne le : {profession}. {lire_texte('militaire.txt')}"
        elif profession == "fisc":
            message = f"cette rubrique concerne le : {profession}. {lire_texte('fisc.txt')}"
        elif profession == "cadastre":
            message = f"cette rubrique concerne le : {profession}. {lire_texte('cadastre.txt')}"   
        elif profession == "police":
            message = f"cette rubrique concerne le : {profession}. {lire_texte('police.txt')}"  
        elif profession == "notaire":
            message = f"cette rubrique concerne le : {profession}. {lire_texte('notaire.txt')}"           
        else:
            message = f"cette rubrique n'existe pas : {profession}."
    return render_template("index.html", message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render attribue automatiquement un port
    app.run(host="0.0.0.0", port=port)

