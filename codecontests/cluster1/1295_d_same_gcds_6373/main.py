#!/usr/bin/env python3
from library import gcd, euler_totient

for _ in range(int(input())):
    a, m = map(int, input().split())
    g = gcd(a, m)
    m = m // g
    print(euler_totient(m))