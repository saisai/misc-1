from PIL import Image


X, Y = 3, 2

#im = open('/Users/ilan/cas-installer/cas_installer/nsis/continuum_nsis_header.bmp')
im = Image.open('/Users/ilan/Downloads/heather-hope.jpg')
im = im.resize((200, 300))

a = im.copy()
b = im.transpose(Image.FLIP_LEFT_RIGHT)
c = im.transpose(Image.FLIP_TOP_BOTTOM)
d = im.rotate(180)

w, h = a.size
im2 = im.resize((2 * w, 2 * h))
print a.size
print im2.size

im2.paste(a, box=(0, 0))
im2.paste(b, box=(w, 0))
im2.paste(c, box=(0, h))
im2.paste(d, box=(w, h))

w, h = im2.size
im3 = im2.resize((X * w, Y * h))
for x in range(X):
    for y in range(Y):
        im3.paste(im2, box=(x * w, y * h))

im3.show()
#im3.save('hope.png')
