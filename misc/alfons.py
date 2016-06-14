from math import cos, tan, pi


def height(r, a, verbose=False):
    phi = (1.5 * a / r) ** (1.0 / 3.0)
    h = 0.5 * (phi ** 2.0) * r
    if verbose:
        print('h =', h)
        print(phi * r)

    phi_l = 0
    phi_r = pi / 4.0
    for i in range(100):
        phi_m = 0.5 * (phi_l + phi_r)
        if tan(phi_m) * r > phi_m * r + 0.5 * a:
            phi_r = phi_m
        else:
            phi_l = phi_m
    if verbose:
        print(phi_m)
        print('h =', r * (1.0 / cos(phi_m) - 1))
    #    print 9.0 * (a ** 2) * r / (32.0 * h ** 3)
    return h


if __name__ == '__main__':
    #for i in [1]:#xrange(-10,10):
    print(height(6.375e6, 1))
