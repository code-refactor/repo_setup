#!/usr/bin/env python3

from library import fast_input, DisjointSetUnion

def read_line():
    return fast_input().strip()

# Read the number of passwords
n = int(read_line())

# Create a DSU with 26 letters (a-z)
dsu = DisjointSetUnion(26)

# Track which letters are used in any password
used_letters = [False] * 26

# Process each password
for _ in range(n):
    password = read_line()
    
    # Get unique letters in the password
    letters = set(password)
    
    # Mark letters as used
    for letter in letters:
        letter_idx = ord(letter) - ord('a')
        used_letters[letter_idx] = True
    
    # Connect all letters in the same password
    if len(letters) > 1:
        first_letter = ord(next(iter(letters))) - ord('a')
        for letter in letters:
            letter_idx = ord(letter) - ord('a')
            dsu.union(first_letter, letter_idx)

# Count the number of distinct connected components (password groups)
groups = set()
for i in range(26):
    if used_letters[i]:
        groups.add(dsu.find(i))

# The result is the number of distinct password groups
print(len(groups))