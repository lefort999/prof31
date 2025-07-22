from flask import Flask, render_template, request

app = Flask(__name__)

rubriques = ['enigme', 'fisc', 'tiers-état']
professions = ['militaire', 'chanvrier', 'douanier']

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        rubrique = request.form.get('rubrique')
        profession = request.form.get('profession')

        if not rubrique or not profession:
            message = "⚠️ Veuillez sélectionner une rubrique ET une profession."
        else:
            message = f"🔎 Résultats pour : rubrique **{rubrique.capitalize()}** et profession **{profession.capitalize()}**."

    return render_template('index.html', rubriques=rubriques, professions=professions, message=message)

if __name__ == '__main__':
    app.run(debug=True)
