import re


NAME_TO_HEX = {
        'aqua': '#0ff',
        'black': '#000',
        'blue': '#00f',
        'fuchsia': '#f0f',
        'lime': '#0f0',
        'white': '#fff',
        'yellow': '#ff0'
        }


HEX_TO_NAME = {
        '#808080': 'gray',
        '#008000': 'green',
        '#800000': 'maroon',
        '#000080': 'navy',
        '#8080000': 'olive',
        '#800080': 'purple',
        '#f00': 'red',
        '#c0c0c0': 'silver',
        '#008080': 'teal'
        }


def _rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def color_shortcut(color):
    color = color.lower()

    # 'grey' and 'gray' are synonyms im most browsers, use 'gray' for correct
    # behaviour in IE
    if color == 'grey':
        color = 'gray'

    # Try converting RGB to hexadecimal, which is always shorter
    rgb = re.search(r'^rgb\((\d{1,3}), (\d{1,3}), (\d{1,3})\)$', color)

    if rgb:
        color = _rgb_to_hex(map(int, rgb.groups()))

    # Check if hexadecimal code
    hexa = re.search(r'^#([a-z0-9]{6})$', color)

    if hexa:
        code = hexa.group(1)

        # Check if a 3-character variant is possible, e.g. 11ff00 -> 1f0
        if code[0] == code[1] and code[2] == code[3] and code[4] == code[5]:
            color = '#' + code[0] + code[2] + code[4]

        # Try to replace long hexadecimals with shorter color names
        if color in HEX_TO_NAME:
            return HEX_TO_NAME[color]
    elif color in NAME_TO_HEX:
        # Long color names can be replaced with shorted hexadecimal codes
        return NAME_TO_HEX[color]

    return color
