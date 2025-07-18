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

# 🔹 Professions spécifiques avec messages personnalisés
PROFESSIONS_SPECIFIQUES = {
    "douanier": "Le dossier de retraite se trouve aux Archives nationales sous la cote R12 pour la période 1780–1820.",
    "fonctionnaire": "Le dossier se trouve dans le ministère concerné.",
    "soldat": "On trouve des états des troupes dès 1700.",
    "chapelier": "L'intronisation était accompagnée d'une 'messe du diable', interdite vers 1770.",
    "chanvrier": "Cette profession était souvent exercée par tout un village.",
    "prof33": "Texte à insérer ici pour prof33. Tu peux le modifier librement."
}

# 🔹 Causes de décès avec messages (à compléter)
CAUSES_DECES = {
    "suicide": "xxxxxxxxx",
    "mort naturelle": "xxxxxxxxx",
    "blessure": "xxxxxxxxx",
    "meurtre": "xxxxxxxxx",
    "cause inconnue": "xxxxxxxxx",
    "disparition": "xxxxxxxxx"
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

# 🔹 Route principale avec traitement des trois boîtes
@app.route("/", methods=["GET", "POST"])
def recherche():
    message = ""
    if request.method == "POST":
        profession = request.form.get("profession")
        prof_spec = request.form.get("prof_spec")
        cause_deces = request.form.get("cause_deces")

        if profession in PROFESSIONS:
            message += f"\nRubrique générale :\n{lire_texte(PROFESSIONS[profession])}\n\n"

        if prof_spec in PROFESSIONS_SPECIFIQUES:
            message += f"Profession spécifique : {prof_spec.capitalize()} → {PROFESSIONS_SPECIFIQUES[prof_spec]}\n\n"

        if cause_deces in CAUSES_DECES:
            message += f"Cause de décès : {cause_deces.capitalize()} → {CAUSES_DECES[cause_deces]}\n"

    return render_template("index.html",
                           message=message,
                           professions=PROFESSIONS.keys(),
                           profs_spec=PROFESSIONS_SPECIFIQUES.keys(),
                           causes=CAUSES_DECES.keys())

# 🔹 Lancement du serveur
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
