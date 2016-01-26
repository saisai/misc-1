from random import randint

from PIL import Image
import cv2
import numpy


a = Image.open('beach.jpg')
a = a.resize((1280, 960))
print a.size
width, height = a.size
frames = 600

video = cv2.VideoWriter('out.avi',
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                        10, (width, height), True)

for t in xrange(frames):
    f = 1.0 * t / (frames - 1)
    r = 100
    m = int(50.0 * (1.0 - f))
    print '%3d %10.3f %10.3f' % (t, f, r)
    b = a.copy()
    for unused in xrange(1000):
        x = randint(0, width - r)
        y = randint(0, height - r)
        c = b.crop(box=(x, y, x+r, y+r))
        b.paste(c, box=(x + randint(-m, m), y + randint(-m, m)))

    c = numpy.array(b.convert('RGB'))
    c = c[:, :, ::-1].copy()
    video.write(c)

cv2.destroyAllWindows()
video.release()
