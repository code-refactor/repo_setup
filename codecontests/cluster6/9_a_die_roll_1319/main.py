#!/usr/bin/env python3

from library import fraction_to_string

x, y = map(int, input().split())
z = 7 - max(x, y)
print(fraction_to_string(z, 6))
