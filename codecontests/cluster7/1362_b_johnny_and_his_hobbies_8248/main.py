#!/usr/bin/env python3

from library import read_int, read_array, find_k

t = read_int()
for _ in range(t):
    n = read_int()
    arr = read_array()
    
    # Find smallest k such that s^k for all s in set equals the original set
    k = find_k(arr)
    print(k)