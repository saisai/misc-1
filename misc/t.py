from random import randint

from PIL.Image import open

z = 30

a = open('/Users/ilan/Desktop/moit.png')
w, h = a.size
for unused in xrange(1000):
    x = randint(0, w-100)
    y = randint(0, h-100)
    b = a.crop(box=(x, y, x+100, y+100))
    a.paste(b, box=(x + randint(-z, z), y + randint(-z, z)))
#a.show()
a.save('out.jpg')
