from flask import Flask, render_template, jsonify
from urllib.request import Request, urlopen
import json
from datetime import datetime
import time

app = Flask(__name__)
app.config['DEBUG'] = True

# ----------------------------
# Page d'accueil
# ----------------------------
@app.route('/')
def hello_world():
    return render_template('hello.html')

# ----------------------------
# Page contact
# ----------------------------
@app.route('/contact/')
def contact():
    return render_template("contact.html")

# ----------------------------
# API météo Tawarano
# ----------------------------
@app.route('/tawarano/')
def meteo():
    url = 'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'
    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': round(temp_day_value, 2)})

    return jsonify(results=results)

# ----------------------------
# Page graphique
# ----------------------------
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# ----------------------------
# Page histogramme
# ----------------------------
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# ----------------------------
# API commits GitHub avec cache + User-Agent
# ----------------------------
cached_commits = None
last_fetch = 0

@app.route('/commits-data/')
def commits_data():
    url = 'https://api.github.com/repos/Mariecls/5MCSI_Metriques/commits?per_page=20'
    global cached_commits, last_fetch

    # Si cache récent (<1h), on le renvoie
    if cached_commits and (time.time() - last_fetch < 3600):
        return jsonify(cached_commits)

    try:
        # Lecture du fichier local comme fallback pour ne pas dépasser la limite
        with open('commits_local.json', 'r') as f:
            commits = json.load(f)
    except FileNotFoundError:
        # Si fichier local absent, on essaye GitHub (risque de 403)
        try:
            response = urlopen(url)
            raw = response.read()
            commits = json.loads(raw.decode("utf-8"))
        except Exception as e:
            return jsonify({'error': 'Erreur lors de la récupération des commits', 'details': str(e)}), 503

    # Transformation en minutes
    minutes_list = []
    for commit in commits:
        date_string = commit.get('commit', {}).get('author', {}).get('date')
        if date_string:
            try:
                date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
                minutes_list.append(date_object.minute)
            except Exception:
                continue

    minutes_count = Counter(minutes_list)
    results = [{'minute': m, 'count': minutes_count.get(m, 0)} for m in range(60)]

    cached_commits = {"results": results}
    last_fetch = time.time()

    return jsonify(cached_commits)

# ----------------------------
# Page graphique des commits
# ----------------------------
@app.route('/commits/')
def commits():
    return render_template('commits.html')

# ----------------------------
# Pour Alwaysdata
# ----------------------------
application = app

if __name__ == "__main__":
    app.run(debug=True)
