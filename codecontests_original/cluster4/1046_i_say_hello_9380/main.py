#!/usr/bin/env python3

from sys import stdin

stdin = iter(stdin)

class Vector:
    ''''''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def dot(self, vec2):
        return self.x * vec2.x + self.y * vec2.y

    def cross(self, vec2):
        return self.x * vec2.y - self.y * vec2.x

    def norm_square(self):
        return self.dot(self)

    def __str__(self):
        return str((self.x, self.y))

    __radd__ = __add__
    __rsub__ = __sub__

def min_distnace_less_than_d1(ab1: Vector, ab2: Vector, d1: int):
    ''' '''
    L = ab2 - ab1
    proj1 = ab1.dot(L)
    proj2 = ab2.dot(L)
    between = (proj1 * proj2 < 0)
    if between:
        # altitude is minimum
        # return altitude < d
        # return |ab1.cross(L)| / sqrt(L.norm_square()) < d
        return ab1.cross(L)**2 <= d1**2 * L.norm_square()
    else:
        # minimum edge is minimum distnace
        minSquare = min([ab1.norm_square(), ab2.norm_square()])
        return minSquare <= d1**2


if __name__ == "__main__":
    N = int(next(stdin))
    d1, d2 = (int(x) for x in next(stdin).split())
    ABs = []
    for _ in range(N):
        Ax, Ay, Bx, By = (int(x) for x in next(stdin).split())
        ABs.append(Vector(Bx, By) - Vector(Ax, Ay))

    resetState = True
    count = 0

    for i in range(len(ABs)-1):
        ab1, ab2 = ABs[i:i+2]
        if resetState and min_distnace_less_than_d1(ab1, ab2, d1):
            count += 1
            resetState = False

        resetState = resetState or (ab2.norm_square() > d2**2)

    print(count)
