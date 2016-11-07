import json
import math
import random


def all_random(x, y):
    return random.random() * 20.0


def simple_sine(x, y):
    return math.sin(x) * 5.0 + math.sin(y) * 5.0


STYLES = {
    'random': all_random,
    'sine': simple_sine,
}


def value(x, y, style):
    return STYLES[style](x, y)


def generate(width=20, height=20, style='sine'):
    values = []

    for x in range(width):
        for y in range(height):
            values.append(value(x, y, style))

    return {
        'width': width,
        'height': height,
        'values': values,
    }


if __name__ == '__main__':
    data = generate()

    with open('output.json', 'w') as out:
        json.dump(data, out)
