import json

from flask import Flask, render_template, send_from_directory

import generate


app = Flask(__name__)


@app.route('/')
def render():
    return render_template('render.html')


@app.route('/js/<path:path>/')
def js(path):
    return send_from_directory('js', path)


@app.route('/data/<style>/')
def output(style):
    return json.dumps(generate.generate(style=style))

app.run('127.0.0.1', 8088, debug=True)
