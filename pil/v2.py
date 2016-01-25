from random import randint

from PIL import ImageDraw, Image
import cv2
import numpy


a = Image.open('cf.jpg')
width, height = a.size
frames = 600

video = cv2.VideoWriter('out.avi',
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                        10, (width, height), True)

for t in xrange(frames):
    f = 1.0 * t / (frames - 1)
    r = 30.0 * (1.0 - f)
    print '%3d %10.3f %10.3f' % (t, f, r)
    b = a.copy()
    d = ImageDraw.Draw(b)
    for unused in xrange(5000):
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        c = b.getpixel((x, y))
        d.ellipse((x-r, y-r, x+r, y+r), fill=c)

    c = numpy.array(b.convert('RGB'))
    c = c[:, :, ::-1].copy()
    video.write(c)

cv2.destroyAllWindows()
video.release()
