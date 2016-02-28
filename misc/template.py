import re
import sys


def fill_template(data, d):
    pat = re.compile(r'__(\w+)__')

    def replace(match):
        key = match.group(1)
        return d.get(key, match.group(0))

    return pat.sub(replace, data)


if __name__ == '__main__':
    DATA = """\
My name is __NAME__!
I am __AGE__ years old.

__FOO__

Sincerely __NAME__
"""
    print fill_template(DATA,
                        {'NAME': 'Ilan', 'AGE': '44', 'SEX': 'male'})
