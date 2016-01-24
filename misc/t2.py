from string import uppercase
from random import randint, choice

from PIL.Image import open
from PIL import ImageDraw, ImageFont, ImageOps

z = 20

a = open('/Users/ilan/Desktop/moit.png')
w, h = a.size
for unused in xrange(0):#10000):
    s = randint(100, 400)
    x = randint(0, w - s)
    y = randint(0, h - s)
    b = a.crop(box=(x, y, x + s, y + s))
    #b = b.resize((75, 75))
    #if randint(0, 2) == 0:
    b = ImageOps.invert(b)
    a.paste(b, box=(x + randint(-z, z), y + randint(-z, z)))
#a = ImageOps.invert(a)

d = ImageDraw.Draw(a)
#for unused in xrange(2000):
#    x = randint(0, w-1)
#    y = randint(0, h-1)
#    c = a.getpixel((x, y))
#    d.ellipse((x-15, y-15, x+15, y+15), fill=c)
path = '/Users/ilan/python/pkgs/matplotlib-1.5.1-np110py27_0/lib/python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/Vera.ttf'
font = ImageFont.truetype(path, 50)

for unused in xrange(10000):
    x = randint(0, w-1)
    y = randint(0, h-1)
    c = a.getpixel((x, y))
    d.text((x-10, y-10), choice(uppercase), fill=c, font=font)

a.show()
#a.save('out.jpg')
