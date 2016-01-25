from string import uppercase
from random import randint, choice

from PIL.Image import open
from PIL import ImageDraw, ImageFont


def letterize(im, n=10000, font=None):
    if font is None:
        path = '/Users/ilan/python/pkgs/matplotlib-1.5.1-np110py27_0/lib/python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/Vera.ttf'
        font = ImageFont.truetype(path, 50)

    d = ImageDraw.Draw(im)
    w, h = im.size
    for unused in xrange(n):
        x = randint(0, w-1)
        y = randint(0, h-1)
        c = a.getpixel((x, y))
        d.text((x-10, y-10), choice(uppercase), fill=c, font=font)


a = open('/Users/ilan/Downloads/heather-hope.jpg')
letterize(a)
a.save('letters.png')
