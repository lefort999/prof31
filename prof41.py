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
    "orfèvre": "orfèvre.txt"
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
        return "❌ Fichier non trouvé."

@app.route("/", methods=["GET", "POST"])
def recherche():
    message = ""

    try:
        if request.method == "POST":
            rubrique = request.form.get("rubrique")
            profession = request.form.get("profession")
            caracteristique = request.form.get("caracteristique")
            lieu = request.form.get("lieu", "").lower()
            code_postal = request.form.get("code_postal", "")
            date_min = request.form.get("date_min")
            circonstance = request.form.get("circonstance", "").lower()

            naissance = None
            try:
                naissance = int(date_min) if date_min else None
            except ValueError:
                pass  # Si la date est incorrecte, on ignore

            # ▶ Ajout des résultats
            if rubrique in RUBRIQUES:
                message += f"📁 Rubrique sélectionnée : {rubrique.capitalize()}\n"
                message += lire_texte(RUBRIQUES[rubrique]) + "\n"

            if profession in PROFESSIONS:
                message += f"\n👤 Profession sélectionnée : {profession.capitalize()}\n"
                message += lire_texte(PROFESSIONS[profession]) + "\n"

            if caracteristique in CARACTERISTIQUE:
                message += f"\n🔍 Caractéristique sélectionnée : {caracteristique.capitalize()}\n"
                message += lire_texte(CARACTERISTIQUE[caracteristique]) + "\n"

            # ▶ Analyse contextuelle
            msg = []

            militaire = profession == "militaire"
            texte_prof = lire_texte(PROFESSIONS.get(profession, "")) if profession else ""
            texte_rub = lire_texte(RUBRIQUES.get(rubrique, "")) if rubrique else ""

            officier = "officier" in texte_prof
            blesse = "blessé" in texte_prof
            celibataire = "célibataire" in texte_rub
            etatcivil = "acte" in texte_rub

            if profession == "douanier":
                msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

            if rubrique == "Alsace":
                msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : consulter ANOM ou archives allemandes.")

            if profession == "orfèvre":
                if lieu.lower() == "paris":
                    msg.append("💎 Orfèvre parisien : consulter les registres de poinçons de la capitale.")
                else:
                    msg.append("💎 Orfèvre en province : consulter les registres de poinçons régionaux, ils sont différents de ceux de Paris.")

            if circonstance == "inondation":
                msg.append("🌊 En 1910 Paris sous les eaux.")

            if militaire and (blesse or officier):
                msg.append("🎖️ Militaire blessé/officier : consulter les registres militaires.")

            if celibataire and etatcivil:
                msg.append("📜 Célibataire avec acte complet : voir actes notariés et mentions marginales.")

            if msg:
                message += "\n🔎 Analyse complémentaire :\n" + "\n".join(msg)

    except Exception as e:
        message = f"🚨 Une erreur s'est produite : {str(e)}"

    return render_template("index.html",
                           message=message,
                           rubriques=RUBRIQUES.keys(),
                           professions=PROFESSIONS.keys(),
                           caracteristique=CARACTERISTIQUE.keys())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)