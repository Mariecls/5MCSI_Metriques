from flask import Flask, render_template
from datetime import datetime
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/contact/')
def ma_premiere_api():
    return "<h2>Ma page de contact</h2>"

if __name__ == "__main__":
    app.run(debug=True)
