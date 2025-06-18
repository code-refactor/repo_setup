"""
Library file for cluster1.
This contains shared code that can be imported by problems in this cluster.
"""
import math
from functools import reduce
from collections import Counter

# Basic operations
def gcd(a, b):
    """Calculate the greatest common divisor of two numbers."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate the least common multiple of two numbers."""
    return a * b // gcd(a, b)

def extended_gcd(a, b):
    """Extended Euclidean algorithm to find coefficients x, y such that ax + by = gcd(a, b)."""
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    """Calculate the modular multiplicative inverse of a with respect to modulus m."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

# Primality and divisibility
def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_divisors(n):
    """Find all divisors of a number efficiently."""
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

def count_divisors(n):
    """Count the number of divisors of a number."""
    return len(find_divisors(n))

def prime_factorization(n):
    """Return list of prime factors (with repetition)."""
    factors = []
    # Handle factor 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Handle odd factors
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    if n > 1:  # If n is a prime number greater than 2
        factors.append(n)
    return factors

def unique_prime_factors(n):
    """Return list of unique prime factors."""
    return list(set(prime_factorization(n)))

def find_smallest_prime_factor(n):
    """Find the smallest prime factor of n."""
    if n <= 1:
        return n
    if n % 2 == 0:
        return 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i
        i += 2
    return n  # n is prime

def find_first_k_factors(n, k):
    """Find first k factors of n (excluding 1)."""
    factors = []
    i = 2
    temp_n = n
    while len(factors) < k and i * i <= temp_n:
        if temp_n % i == 0:
            factors.append(i)
            temp_n //= i
            if len(factors) == k - 1 and temp_n > 1:
                factors.append(temp_n)
                break
        else:
            i += 1
    return factors if len(factors) == k else []

# Advanced number theory
def euler_totient(n):
    """Calculate Euler's totient function φ(n)."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def legendre_formula(n, p):
    """Count the highest power of prime p that divides n!."""
    count = 0
    power = p
    while power <= n:
        count += n // power
        power *= p
    return count

def is_power_of_two_minus_one(n):
    """Check if n is of the form 2^k - 1."""
    return (n + 1) & n == 0 and n > 0

# Modular arithmetic
def mod_pow(base, exp, mod):
    """Calculate (base^exp) % mod efficiently."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def mod_add(a, b, mod):
    """Calculate (a + b) % mod."""
    return (a % mod + b % mod) % mod

def mod_mul(a, b, mod):
    """Calculate (a * b) % mod."""
    return ((a % mod) * (b % mod)) % mod

def mod_div(a, b, mod):
    """Calculate (a / b) % mod (using modular inverse)."""
    return mod_mul(a, mod_inverse(b, mod), mod)

# Utility functions
def arithmetic_series_sum(first, diff, terms):
    """Calculate sum of arithmetic series."""
    return (terms * (2 * first + (terms - 1) * diff)) // 2

def geometric_series_sum(first, ratio, terms):
    """Calculate sum of geometric series."""
    if ratio == 1:
        return first * terms
    return first * (1 - ratio**terms) // (1 - ratio)

def geometric_series_infinite_sum(first, ratio):
    """Calculate sum of infinite geometric series (|ratio| < 1)."""
    if abs(ratio) >= 1:
        raise ValueError("Ratio must be less than 1 for infinite sum")
    return first / (1 - ratio)

def factor_counter(n):
    """Return a Counter object with prime factors as keys and their powers as values."""
    return Counter(prime_factorization(n))