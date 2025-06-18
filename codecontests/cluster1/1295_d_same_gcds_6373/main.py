#!/usr/bin/env python3
from library import gcd, euler_totient

def solve():
    a, m = map(int, input().split())
    
    # Find gcd(a, m)
    g = gcd(a, m)
    
    # Calculate m' = m / gcd(a, m)
    m_prime = m // g
    
    # The answer is Euler's totient function φ(m')
    return euler_totient(m_prime)

t = int(input())
for _ in range(t):
    print(solve())