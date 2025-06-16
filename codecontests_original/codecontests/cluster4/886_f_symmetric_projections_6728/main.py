#!/usr/bin/env python3

from fractions import Fraction
import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()

    def __hash__(self):
        return hash(self.to_tuple())

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return self+(-other)

    def scalar_mul(self, mu):
        return Point(mu*self.x, mu*self.y)

    def int_divide(self, den):
        return Point(self.x//den, self.y//den)


class Line:
    def __init__(self, a, b, c):
        # ax+by+c=0
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return "{}*x + {}*y + {} = 0".format(self.a, self.b, self.c)

    @classmethod
    def between_two_points(cls, P, Q):
        return cls(P.y-Q.y, Q.x-P.x, P.x*Q.y-P.y*Q.x)

    def evaluate(self, P):
        return self.a*P.x+self.b*P.y+self.c

    def direction(self):
        if self.a == 0:
            return (0, 1)
        return (1, Fraction(self.b, self.a))


def abs_sgn(x):
    if x == 0:
        return 0, 0
    if x < 0:
        return -x, -1
    return x, 1


def solve(tuple_points):
    points = set()
    center = Point(0, 0)
    for cur in tuple_points:
        cur = Point(*cur).scalar_mul(2*n)
        center += cur
        points.add(cur)

    center = center.int_divide(n)
    dcenter = center+center

    sym_points_set = set()
    for p in points:
        sym_points_set.add(dcenter-p)
    nosym = list(points - sym_points_set)

    if len(nosym) == 0:
        print(-1)
        exit(0)

    p0 = nosym[0]
    good_lines = set()
    for p in nosym:
        m = (p+p0).int_divide(2)
        line = Line.between_two_points(m, center)
        distances = list(map(line.evaluate, nosym))

        ok = True
        mydict = {}
        for dd in distances:
            dda, sgn = abs_sgn(dd)
            if dda not in mydict:
                mydict[dda] = sgn
            else:
                mydict[dda] += sgn
        for k in mydict:
            if mydict[k] != 0:
                ok = False
                break
        if ok:
            good_lines.add(line.direction())

    return len(good_lines)


# This one is accepted on CF
if __name__ == "__main__":
    n = int(input())
    pts = []
    for i in range(n):
        row = input().split(" ")
        cur = (int(row[0]), int(row[1]))
        pts.append(cur)
    print(solve(pts))
