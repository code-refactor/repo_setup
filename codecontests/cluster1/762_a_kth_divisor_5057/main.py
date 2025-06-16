#!/usr/bin/env python3
from library import get_divisors

n, k = map(int, input().split())
result = get_divisors(n)
if k > len(result):
    print(-1)
else:
    print(result[k-1])