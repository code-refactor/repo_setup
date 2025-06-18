#!/usr/bin/env python3

from sys import stdin
from library import Vector

stdin = iter(stdin)

def min_distance_less_than_d1(ab1, ab2, d1):
    L = ab2 - ab1
    proj1 = ab1.dot(L)
    proj2 = ab2.dot(L)
    between = (proj1 * proj2 < 0)
    if between:
        # altitude is minimum
        # return |ab1.cross(L)| / sqrt(L.norm_square()) < d
        return ab1.cross(L)**2 <= d1**2 * L.norm_square()
    else:
        # minimum edge is minimum distance
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
        if resetState and min_distance_less_than_d1(ab1, ab2, d1):
            count += 1
            resetState = False

        resetState = resetState or (ab2.norm_square() > d2**2)

    print(count)