"""
Competitive Programming Library for Cluster 6
Optimized for math, combinatorics, and probability problems
"""

import math
import sys
from fractions import Fraction

MOD = 10**9 + 7
MOD2 = 998244353

def fast_power(base, exp, mod=MOD):
    """Fast modular exponentiation"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

def mod_inverse(a, mod=MOD):
    """Modular inverse using Fermat's little theorem (mod must be prime)"""
    return fast_power(a, mod - 2, mod)

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse_general(a, mod):
    """Modular inverse for any modulus using extended GCD"""
    gcd, x, y = extended_gcd(a, mod)
    if gcd != 1:
        return None
    return (x % mod + mod) % mod

class Combinatorics:
    """Precomputed factorials and combinatorial functions"""
    
    def __init__(self, max_n=200200, mod=MOD, use_mod=True):
        self.mod = mod
        self.max_n = max_n
        self.use_mod = use_mod
        self.fact = [1] * (max_n + 1)
        
        if use_mod:
            self.inv_fact = [1] * (max_n + 1)
            for i in range(1, max_n + 1):
                self.fact[i] = (self.fact[i-1] * i) % mod
            
            self.inv_fact[max_n] = mod_inverse(self.fact[max_n], mod)
            for i in range(max_n - 1, -1, -1):
                self.inv_fact[i] = (self.inv_fact[i+1] * (i+1)) % mod
        else:
            for i in range(1, max_n + 1):
                self.fact[i] = self.fact[i-1] * i
    
    def C(self, n, k):
        """Binomial coefficient nCk"""
        if k < 0 or k > n or n < 0:
            return 0
        if self.use_mod:
            return (self.fact[n] * self.inv_fact[k] % self.mod) * self.inv_fact[n-k] % self.mod
        else:
            return self.fact[n] // (self.fact[k] * self.fact[n-k])
    
    def P(self, n, k):
        """Permutation nPk"""
        if k < 0 or k > n or n < 0:
            return 0
        if self.use_mod:
            return self.fact[n] * self.inv_fact[n-k] % self.mod
        else:
            return self.fact[n] // self.fact[n-k]

def gcd(a, b):
    """Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Least Common Multiple"""
    return a * b // gcd(a, b)

def reduce_fraction(num, den):
    """Reduce fraction to lowest terms"""
    if den == 0:
        return None
    g = gcd(abs(num), abs(den))
    return num // g, den // g

def fraction_to_string(num, den):
    """Convert fraction to string format"""
    num, den = reduce_fraction(num, den)
    if den == 1:
        return str(num)
    return f"{num}/{den}"

class FastIO:
    """Fast input/output utilities"""
    
    @staticmethod
    def read_int():
        return int(sys.stdin.readline())
    
    @staticmethod
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    @staticmethod
    def read_string():
        return sys.stdin.readline().strip()
    
    @staticmethod
    def solve_multiple_cases(solve_func):
        """Handle multiple test cases"""
        t = int(input())
        for _ in range(t):
            solve_func()

def probability_sum(probs):
    """Sum probabilities avoiding floating point errors"""
    total = sum(probs)
    return min(1.0, total)

def expected_value(values, probs):
    """Calculate expected value given values and probabilities"""
    return sum(v * p for v, p in zip(values, probs))
