from random import randint

from PIL import ImageDraw, Image
import cv2
import numpy


width, height = 600, 800
frames = 600

video = cv2.VideoWriter('out.avi',
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                        20, (width, height), True)

a = Image.open('/Users/ilan/Desktop/moit.png')
x0, y0 = 100, 300
r = 10

a = a.crop(box=(x0, y0, x0 + width, y0 + height))
for t in xrange(frames):
    print t
    b = a.copy()
    d = ImageDraw.Draw(b)
    for unused in xrange((frames-1-t) * 10):
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        c = b.getpixel((x, y))
        d.ellipse((x-r, y-r, x+r, y+r), fill=c)

    c = numpy.array(b.convert('RGB'))
    c = c[:, :, ::-1].copy()
    video.write(c)

cv2.destroyAllWindows()
video.release()
