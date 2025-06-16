#!/usr/bin/env python3

from functools import lru_cache

s = input() + ' '
suffixes = set()

@lru_cache(maxsize=None)
def gen(left, right):
    if left > 6:
        suffixes.add(s[left - 2:left])
        if s[left - 2:left] != s[left:right]:
            gen(left - 2, left)
    if left > 7:
        suffixes.add(s[left - 3:left])
        if s[left - 3:left] != s[left:right]:
            gen(left - 3, left)

gen(len(s) - 1, len(s))
print(len(suffixes))
print('\n'.join(sorted(suffixes)))
 