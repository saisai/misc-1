import re
import sys


def simple_template(data, d):
    pat = re.compile(r'__(\w+)__')

    def replace(match):
        key = match.group(1)
        try:
            return d[key]
        except KeyError:
            sys.exit("Error: did not find key '%s' in dict" % key)

    return pat.sub(replace, data)


if __name__ == '__main__':
    DATA = """\
My name is __NAME__!
I am __AGE__ years old.

Sincerely __NAME__
"""
    print simple_template(DATA,
                          {'NAME': 'Ilan', 'AGE': '44', 'SEX': 'male'})
