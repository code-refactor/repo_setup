#!/usr/bin/env python3

from library import create_2d_table
from math import inf

a, b = input(), input()
na, nb = len(a), len(b)

# Precompute next occurrence of each character from each position
next_pos = create_2d_table(na + 1, 26, -1)

for i in range(na - 1, -1, -1):
    for j in range(26):
        next_pos[i][j] = next_pos[i + 1][j]
    next_pos[i][ord(a[i]) - ord('a')] = i

pos = 0
copies = 1

for char in b:
    char_idx = ord(char) - ord('a')
    
    if pos == na:  # Need new copy of string a
        copies += 1
        pos = 0
    
    if next_pos[pos][char_idx] == -1:  # Character not found from current position
        copies += 1
        pos = 0
        if next_pos[pos][char_idx] == -1:  # Character not in string a at all
            copies = inf
            break
    
    pos = next_pos[pos][char_idx] + 1

print(copies if copies != inf else -1)    
