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
    "militaire": "militaire.txt",
    "orfèvre": "orfèvre.txt"  # ajouté si tu veux cette analyse
}

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
        lieu = request.form.get("lieu", "").lower()
        code_postal = request.form.get("code_postal")
        date_min = request.form.get("date_min")
        date_max = request.form.get("date_max")

        try:
            naissance = int(date_min) if date_min else None
        except ValueError:
            naissance = None

        prof = profession

        if rubrique in RUBRIQUES:
            message += f"📁 Rubrique sélectionnée : {rubrique.capitalize()}\n"
            message += lire_texte(RUBRIQUES[rubrique]) + "\n"

        if profession in PROFESSIONS:
            message += f"\n👤 Profession sélectionnée : {profession.capitalize()}\n"
            message += lire_texte(PROFESSIONS[profession]) + "\n"

        if caracteristique in CARACTERISTIQUE:
            message += f"\n🔍 Caractéristique sélectionnée : {caracteristique.capitalize()}\n"
            message += lire_texte(CARACTERISTIQUE[caracteristique]) + "\n"

        # 🔎 Analyse contextuelle
        msg = []

        militaire = prof == "militaire"
        texte_prof = lire_texte(PROFESSIONS.get(prof, "")) if prof else ""
        texte_rub = lire_texte(RUBRIQUES.get(rubrique, "")) if rubrique else ""

        officier = "officier" in texte_prof
        blesse = "blessé" in texte_prof
        celibataire = "célibataire" in texte_rub
        etatcivil = "acte" in texte_rub
        
        if lieu == "paris" :
            msg.append("📂 la commune .")
            
        if prof == "douanier" :
            msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

         if circonstance == "inondation" :
            msg.append("📂 1910 Paris est sous les eaux .") 
        

        if circonstance == "inondation" :
            msg.append("📂 Paris sous les eaux en 1910 .")

        
        if "alsace" in lieu and naissance and 1870 < naissance < 1918:
            msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : consulter ANOM ou archives allemandes.")

        if prof == "orfèvre" and lieu == "Paris" :
            msg.append("💎 Orfèvre : consulter les registres de poinçons.")

        if militaire and officier and blesse:
            msg.append("🎖️ Militaire blessé/officier : consulter les registres militaires.")

        if celibataire and etatcivil:
            msg.append("📜 Célibataire avec acte complet : voir actes notariés et mentions marginales.")

        if msg:
            message += "\n" + "\n".join(msg)

    return render_template("index.html",
                           message=message,
                           rubriques=RUBRIQUES.keys(),
                           professions=PROFESSIONS.keys(),
                           caracteristique=CARACTERISTIQUE.keys())

# 🔹 Lancement du serveur
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
