from flask import Flask, render_template, jsonify
from urllib.request import urlopen
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
# API commits GitHub avec cache
# ----------------------------
cached_commits = None
last_fetch = 0

@app.route("/commits/")
def commits():
    global cached_commits, last_fetch
    # Utiliser le cache pendant 1 heure
    if cached_commits and (time.time() - last_fetch < 3600):
        return jsonify(cached_commits)

    try:
        url = "https://api.github.com/repos/Mariecls/5MCSI_Metriques/commits"
        response = urlopen(url)
        raw_data = response.read()
        commits_json = json.loads(raw_data.decode("utf-8"))

        results = []
        for commit in commits_json:
            commit_data = commit.get("commit", {}).get("author", {})
            date_str = commit_data.get("date")
            if date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                results.append({
                    "date": date_obj.strftime("%Y-%m-%d %H:%M"),
                    "minute": date_obj.minute
                })

        cached_commits = {"results": results}
        last_fetch = time.time()
        return jsonify(cached_commits)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------
# Page graphique des commits
# ----------------------------
@app.route("/commits-graph/")
def commits_graph():
    return render_template("commits.html")

# ----------------------------
# Pour Alwaysdata
# ----------------------------
application = app

if __name__ == "__main__":
    app.run(debug=True)
