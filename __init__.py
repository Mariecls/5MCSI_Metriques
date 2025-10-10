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
req = Request(api_url, headers={"User-Agent": "metrics-app"})
    with urlopen(req) as resp:
        raw = resp.read()
    payload = json.loads(raw.decode("utf-8"))

    minute_counts = [0] * 60
    for item in payload:
        commit_info = item.get('commit', {})
        author_info = commit_info.get('author', {})
        date_str = author_info.get('date')  # ex: "2024-02-11T11:57:27Z"
        if not date_str:
            continue
        try:
            d = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute_counts[d.minute] += 1
        except Exception:
            continue

    results = [{'minute': i, 'count': minute_counts[i]} for i in range(60)]
    return jsonify(results=results)

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
