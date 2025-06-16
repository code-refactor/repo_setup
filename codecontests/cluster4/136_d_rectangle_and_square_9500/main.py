#!/usr/bin/env python3

import itertools
import sys
from library import dot_product, distance, float_equal

coord = [[]] + [list(map(int, input().split())) for _ in range(8)]

idx = list(range(1, 9))

def perpendicular(v1, v2):
    return float_equal(dot_product(v1, v2), 0, 1e-8)

def all_perpendicular(vs):
    return all([perpendicular(vs[i], vs[(i+1)%4]) for i in range(4)])

def rect_sides(vs):
    ls = [distance((0,0), v) for v in vs]
    return float_equal(ls[0], ls[2], 1e-8) and float_equal(ls[1], ls[3], 1e-8)

def square_sides(vs):
    ls = [distance((0,0), v) for v in vs]
    l = ls[0]
    return all(float_equal(lx, l, 1e-8) for lx in ls)

def coords_to_vecs(cs):
    return [
        [cs[(i+1)%4][0] - cs[i][0], cs[(i+1)%4][1] - cs[i][1]]
        for i in range(4)]

def is_square(coords):
    for p in itertools.permutations(coords):
        vs = coords_to_vecs(p)
        if all_perpendicular(vs) and square_sides(vs):
            return True
    return False

def is_rect(coord):
    for p in itertools.permutations(coord):
        vs = coords_to_vecs(p)
        if all_perpendicular(vs) and rect_sides(vs):
            return True
    return False

for comb in itertools.combinations(idx, 4):
    fsi = list(comb)
    ssi = sorted(list(set(idx) - set(comb)))

    fs = [coord[i] for i in fsi]
    ss = [coord[i] for i in ssi]

    if is_square(fs) and is_rect(ss):
        print("YES")
        print(' '.join(map(str, fsi)))
        print(' '.join(map(str, ssi)))
        sys.exit(0)
    if is_square(ss) and is_rect(fs):
        print("YES")
        print(' '.join(map(str, ssi)))
        print(' '.join(map(str, fsi)))
        sys.exit(0)

print("NO")
