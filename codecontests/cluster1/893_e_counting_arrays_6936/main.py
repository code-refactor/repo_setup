#!/usr/bin/env python3

# 893E - Counting Arrays
from library import prime_factorization, factor_counter, mod_pow
import math

MOD = 10**9 + 7

class Factorial:
    def __init__(self, MOD):
        self.MOD = MOD
        self.factorials = [1, 1]
        self.invModulos = [0, 1]
        self.invFactorial_ = [1, 1]
 
    def calc(self, n):
        if n <= -1:
            return 1
        if n < len(self.factorials):
            return self.factorials[n]
        nextArr = [0] * (n + 1 - len(self.factorials))
        initialI = len(self.factorials)
        prev = self.factorials[-1]
        m = self.MOD
        for i in range(initialI, n + 1):
            prev = nextArr[i - initialI] = prev * i % m
        self.factorials += nextArr
        return self.factorials[n]
 
    def inv(self, n):
        if n <= -1:
            return 1
        p = self.MOD
        pi = n % p
        if pi < len(self.invModulos):
            return self.invModulos[pi]
        nextArr = [0] * (n + 1 - len(self.invModulos))
        initialI = len(self.invModulos)
        for i in range(initialI, min(p, n + 1)):
            next = -self.invModulos[p % i] * (p // i) % p
            self.invModulos.append(next)
        return self.invModulos[pi]
 
    def invFactorial(self, n):
        if n <= -1:
            return 1
        if n < len(self.invFactorial_):
            return self.invFactorial_[n]
        self.inv(n)  # To make sure already calculated n^-1
        nextArr = [0] * (n + 1 - len(self.invFactorial_))
        initialI = len(self.invFactorial_)
        prev = self.invFactorial_[-1]
        p = self.MOD
        for i in range(initialI, n + 1):
            prev = nextArr[i - initialI] = (prev * self.invModulos[i % p]) % p
        self.invFactorial_ += nextArr
        return self.invFactorial_[n]
 
 
class Combination:
    def __init__(self, MOD):
        self.MOD = MOD
        self.factorial = Factorial(MOD)
 
    def ncr(self, n, k):
        if k < 0 or n < k:
            return 0
        k = min(k, n - k)
        f = self.factorial
        return f.calc(n) * f.invFactorial(max(n - k, k)) * f.invFactorial(min(k, n - k)) % self.MOD

def solve():
    t = int(input())
    comb = Combination(MOD)
    
    for _ in range(t):
        x, y = map(int, input().split())
        
        # Get prime factorization using library function
        factor_counts = factor_counter(x)
        
        result = 1
        
        # For each prime factor with its count, calculate combinations
        for prime, count in factor_counts.items():
            # Stars and bars: distributing count powers among y positions
            # C(y + count - 1, count)
            result = (result * comb.ncr(y + count - 1, count)) % MOD
        
        # Multiply by 2^(y-1) for sign choices (first element can be positive or negative,
        # others can be chosen to maintain the product sign)
        result = (result * mod_pow(2, y - 1, MOD)) % MOD
        
        print(result)

solve()