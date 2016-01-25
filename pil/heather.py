from PIL import Image


def four_flip(im):
    a = im.copy()
    b = im.transpose(Image.FLIP_LEFT_RIGHT)
    c = im.transpose(Image.FLIP_TOP_BOTTOM)
    d = im.rotate(180)
    w, h = a.size
    res = im.resize((2 * w, 2 * h))
    res.paste(a, box=(0, 0))
    res.paste(b, box=(w, 0))
    res.paste(c, box=(0, h))
    res.paste(d, box=(w, h))
    return res

def repeat(im, X=1, Y=1):
    w, h = im.size
    res = im.resize((X * w, Y * h))
    for x in range(X):
        for y in range(Y):
            res.paste(im, box=(x * w, y * h))
    return res


im = Image.open('/Users/ilan/Downloads/heather-hope.jpg').resize((200, 300))
im2 = repeat(four_flip(im), 3, 2)
im2.show()
