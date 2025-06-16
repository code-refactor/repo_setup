#!/usr/bin/env python3

from library import DSU, read_int

n = read_int()

# Create DSU for 26 letters
dsu = DSU(26)
used_chars = set()

for _ in range(n):
    s = input().strip()
    chars = list(set(s))  # unique characters in this password
    
    # Mark all characters as used
    for c in chars:
        used_chars.add(ord(c) - ord('a'))
    
    # Union all characters that appear together
    for i in range(len(chars)):
        for j in range(i + 1, len(chars)):
            dsu.union(ord(chars[i]) - ord('a'), ord(chars[j]) - ord('a'))

# Count components among used characters
components = set()
for char_idx in used_chars:
    components.add(dsu.find(char_idx))

print(len(components))