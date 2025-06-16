#!/usr/bin/env python3

from collections import defaultdict

s = input()[5:][::-1]
n = len(s)

suffixes = set()
can2 = [False] * (n + 1)
can3 = [False] * (n + 1)

# Initialize base cases
if n >= 2:
    suffixes.add(s[0:2][::-1])
    can2[2] = True
if n >= 3:
    suffixes.add(s[0:3][::-1])
    can3[3] = True
if n >= 4 and s[0:2] != s[2:4]:
    suffixes.add(s[2:4][::-1])
    can2[4] = True
if n >= 5:
    suffixes.update([s[2:5][::-1], s[3:5][::-1]])
    can2[5] = can3[5] = True

# Dynamic programming for remaining positions
for i in range(6, n + 1):
    if can2[i - 3]:
        suffixes.add(s[i - 3:i][::-1])
        can3[i] = True
    
    if can2[i - 2] and s[i - 2:i] != s[i - 4:i - 2]:
        suffixes.add(s[i - 2:i][::-1])
        can2[i] = True
    
    if can3[i - 2]:
        suffixes.add(s[i - 2:i][::-1])
        can2[i] = True
    
    if can3[i - 3] and s[i - 3:i] != s[i - 6:i - 3]:
        suffixes.add(s[i - 3:i][::-1])
        can3[i] = True

print(len(suffixes))
print('\n'.join(sorted(suffixes)))