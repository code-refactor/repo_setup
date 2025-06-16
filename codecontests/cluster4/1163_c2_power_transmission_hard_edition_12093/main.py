#!/usr/bin/env python3

from itertools import combinations
from library import read_int, read_ints

n = read_int()

points = [tuple(read_ints()) for _ in range(n)]

directions = {}
for pair in combinations(points, 2):
    (x1, y1), (x2, y2) = pair
    if x1 == x2:
        dir = (0, 1)
        b = x1
    else:
        dir = (1, (y2 - y1) / (x2 - x1))
        b = (y2 * x1 - x2 * y1) / (x1 - x2)

    if dir in directions:
        directions[dir].add(b)
    else:
        directions[dir] = set([b])

total_lines = sum(len(value) for key, value in directions.items())

result = 0
for key, value in directions.items():
    current = len(value)
    result += (total_lines - current) * current

print(int(result / 2))
