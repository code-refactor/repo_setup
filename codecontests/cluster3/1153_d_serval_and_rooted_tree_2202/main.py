#!/usr/bin/env python3

from library import read_int, read_ints

n = read_int()
fcs = [0] + read_ints()  # Function type (min/max)
ps = [0, 0] + read_ints()  # Parents

# Mark leaf nodes
cs = [1] * (n + 1)
for i in range(2, n + 1):
    cs[ps[i]] = 0

# Count leaf nodes
nc = sum(cs) - 1

# Bottom-up DP processing
for i in range(n, 1, -1):
    if fcs[ps[i]] == 0:  # MIN operation
        cs[ps[i]] += cs[i]
    else:  # MAX operation
        if not cs[ps[i]]:
            cs[ps[i]] = cs[i]
        else:
            cs[ps[i]] = min(cs[ps[i]], cs[i])

# Calculate result
print(nc - cs[1] + 1)