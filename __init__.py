from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json
from datetime import datetime  

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/contact/')
def ma_premiere_api():
    return render_template("contact.html")

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

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mon_histogramme():
    return render_template("histogramme.html")

from flask import Flask, render_template, jsonify
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True  # Active le debug complet

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/contact/')
def contact():
    return render_template("contact.html")

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

@app.route('/rapport/')
def mongraphique():
    return render_template("graphique.html")

@app.route('/histogramme/')
def mon_histogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/Mariecls/5MCSI_Metriques/commits'
    token = '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' 
    req = Request(url)
    req.add_header('Authorization', f'token {token}')
    try:
        response = urlopen(req)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
    except HTTPError as e:
        return jsonify({'error': f'HTTP Error {e.code}', 'details': e.reason}), 500
    except Exception as e:
        return jsonify({'error': 'Autre erreur', 'details': str(e)}), 500

    results = []
    for commit in json_content:
        try:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            results.append({'minute': date_obj.minute})
        except Exception as e:
            return jsonify({'error': 'Erreur parsing date', 'details': str(e)}), 500

    return jsonify({'results': results})

@app.route('/commits-graph/')
def commits_graph():
    return render_template('commits.html')

if __name__ == "__main__":
    app.run(debug=True)




@app.route('/commits-graph/')
def commits_graph():
    return render_template('commits.html')

if __name__ == "__main__":
    app.run(debug=True)
