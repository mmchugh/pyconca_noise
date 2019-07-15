import json
import math
import random

from opensimplex import OpenSimplex

WIDTH = 20
HEIGHT = 20
tmp = OpenSimplex()


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


power_simplex = OpenSimplex(int(random.random() * 100))


def power(exponent):
    def noise(x, y):
        value = (power_simplex.noise2d(x/3.0, y/3.0) + 1.0) / 2.0

        return (value ** exponent) * 20.0

    return noise


def simplex():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        return (tmp.noise2d(x/3.0, y/3.0) + 1) * 10.0

    return noise


def simple_curve(value):
    start = 0.4
    end = 0.6
    if value < start:
        return 0.0
    if value > end:
        return 1.0
    return (value - start) * (1 / (end - start))


def interpolate(a, b, weight):
    new_weight = simple_curve(weight)

    return a * (1 - new_weight) + b * new_weight


def simple_scurve():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        noise = (tmp.noise2d(x/5.0, y/5.0) + 1) / 2.0

        return interpolate(0.0, 1.0, noise) * 10.0

    return noise


def plains():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        value = (tmp.noise2d(x/3.0, y/3.0) + 1) / 2.0

        value = value**0.25

        value = value - 0.6

        if value < 0:
            value = 0

        return value * 6.0

    return noise


def mountains():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        value = (tmp.noise2d(x*2.0, y) + 1) / 2.0

        value = value

        return value * 20.0

    return noise


def combined():
    m_values = mountains()
    p_values = plains()
    weights = simple_scurve()

    def noise(x, y):
        m = m_values(x, y)
        p = p_values(x, y)
        w = weights(x, y) / 10.0

        return (p * w) + (m * (1 - w))

    return noise


def generate(value):
    values = []

    for x in range(WIDTH):
        for y in range(HEIGHT):
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
