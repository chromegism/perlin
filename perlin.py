import matplotlib.pyplot as plt
import numpy as np
from math import *
from tqdm import tqdm

def generate_vectors(octave):
    """Generate a set of vectors for the given octave"""

    vector_arr = np.random.rand(octave, octave) * 2 * pi

    return vector_arr

def bilinear_interpolation(x, y, points):
    '''Interpolate (x,y) from values associated with four points.

    The four points are a list of four triplets:  (x, y, value).
    The four points can be in any order.  They should form a rectangle.

        >>> bilinear_interpolation(12, 5.5,
        ...                        [(10, 4, 100),
        ...                         (20, 4, 200),
        ...                         (10, 6, 150),
        ...                         (20, 6, 300)])
        165.0

    '''
    # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)

def smoothstep(x, n1, n2):
    """Smoothstep function used to interpolate between numbers"""

    return n1 + (-sin(pi * x + pi / 2) + 1) / 2 * (n2 - n1)

def smoothstep2d(x, y, n1, n2, n3, n4):
    vx = (-sin(pi * x + pi / 2) + 1) / 2
    vy = (-sin(pi * y + pi / 2) + 1) / 2

def interpolate(vectors, size):
    incx = (len(vectors) - 1) / size[0]
    incy = (len(vectors[0]) - 1) / size[1]

    arr = []

    for x in tqdm(range(size[0])):
        arr.append([])
        for y in range(size[1]):
            arr[x].append(bilinear_interpolation(x, y, [(0, 0, vectors[floor(x * incx)]), (1, 0, ), (1, 1, ), (0, 1, )]))

    return arr


if __name__ == '__main__':
    arr = generate_vectors(6)

    plt.imshow(interpolate(arr, [480, 360]), cmap='gray')
    plt.show()