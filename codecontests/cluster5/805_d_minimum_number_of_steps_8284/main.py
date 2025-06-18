#!/usr/bin/env python3

from library import read_str, MOD

def count_steps(s):
    count_a = 0
    total_steps = 0

    for char in s:
        if char == 'a':
            count_a = (count_a * 2) % MOD
            count_a += 1
        elif char == 'b':
            total_steps = (total_steps + count_a) % MOD

    return total_steps

s = read_str()
print(count_steps(s))