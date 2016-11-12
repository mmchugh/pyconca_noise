import json

from flask import Flask, render_template, send_from_directory, request

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
    if style == 'random':
        value_func = generate.all_random
    elif style == 'sine':
        value_func = generate.simple_sine
    elif style == 'octaves':
        # get octaves
        octaves = int(request.args.get('octaves', 4))
        amplitude = int(request.args.get('amplitude', 5))
        value_func = generate.multiple_octaves(octaves, amplitude)
    elif style == 'simplex':
        value_func = generate.simplex()
    elif style == 'power':
        exponent = float(request.args.get('exponent', 1.0))
        value_func = generate.power(exponent)
    elif style == 'scurve':
        value_func = generate.simple_scurve()
    elif style == 'plains':
        value_func = generate.plains()
    elif style == 'mountains':
        value_func = generate.mountains()
    elif style == 'combined':
        value_func = generate.combined()

    return json.dumps(generate.generate(value_func))

app.run('127.0.0.1', 8088, debug=True)
