import json
import math
import random

WIDTH = 20
HEIGHT = 20


def all_random(x, y):
    return random.random() * 20.0


def simple_sine(x, y):
    return math.sin(x) * 5.0 + math.sin(y) * 5.0


def multiple_octaves(octaves, start_amplitude):
    parameters = []
    for i in range(octaves):
        parameters.append({
            'offset': random.random() * 2 * math.pi,
            'frequency': 2**i,
            'amplitude': start_amplitude / float(i+1),
        })

    print parameters

    def noise(x, y):
        value = 0
        for p in parameters:
            x_part = math.sin(
                (x / float(WIDTH))
                * p['frequency']
                * 2 * math.pi
                + p['offset']
            )
            y_part = math.sin(
                (y / float(HEIGHT))
                * p['frequency']
                * 2 * math.pi
                + (x_part % (2 * math.pi))
            )
            value += y_part * p['amplitude']

        return value

    return noise


def generate(value):
    values = []

    for x in range(WIDTH):
        for y in range(WIDTH):
            values.append(value(x, y))

    return {
        'width': WIDTH,
        'height': HEIGHT,
        'values': values,
    }


if __name__ == '__main__':
    data = generate(simple_sine)

    with open('output.json', 'w') as out:
        json.dump(data, out)
