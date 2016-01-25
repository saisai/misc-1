from string import uppercase
from random import randint, choice

from PIL import ImageDraw, ImageFont, Image
import cv2
import numpy


path = '/Users/ilan/python/pkgs/matplotlib-1.5.1-np110py27_0/lib/python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/Vera.ttf'
font = ImageFont.truetype(path, 25)

def letterize(im, n=10000):
    d = ImageDraw.Draw(im)
    w, h = im.size
    for unused in xrange(n):
        x = randint(0, w-1)
        y = randint(0, h-1)
        c = a.getpixel((x, y))
        d.text((x-10, y-10), choice(uppercase), fill=c, font=font)


width, height = 800, 600

video = cv2.VideoWriter('out.avi',
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                        20, (width, height), True)

a = Image.open('/Users/ilan/Downloads/heather-hope.jpg')
for t in xrange(200):
    print t
    b = a.resize((width, height))
    letterize(b, 10 * t)
    c = numpy.array(b.convert('RGB'))
    c = c[:, :, ::-1].copy()
    video.write(c)

cv2.destroyAllWindows()
video.release()
