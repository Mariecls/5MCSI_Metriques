from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('hello.html')  # Assure-toi que hello.html est dans /templates
@app.route('/contact/')
def ma_premiere_api():
    return "<h2>Ma page de contact</h2>"
@app.route('/tawarano/')
def meteo():
    # Remplace 'xxx' par ta clé API si tu testes avec OpenWeatherMap réel
    url = 'https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx'
    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')  # timestamp UNIX
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin → °C
        results.append({'Jour': dt_value, 'temp': round(temp_day_value, 2)})

    return jsonify(results=results)
if __name__ == "__main__":
    app.run(debug=True)
