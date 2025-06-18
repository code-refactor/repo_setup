#!/usr/bin/env python3

from library import read_int, read_array, get_prime_signature, mod_pow
from collections import Counter, defaultdict

# Read input
l = read_int()
numbers = read_array()
c = Counter(numbers)

# Map each number to its prime signature
prime_signatures = defaultdict(int)
for num, count in c.items():
    # Get the prime signature of the number
    signature = get_prime_signature(num)
    prime_signatures[signature] += count

# Dynamic programming to find subsets with square product
dp = defaultdict(int)
dp[0] = 1  # Empty subset has square product

# For each prime signature
for signature in prime_signatures:
    if signature:  # Skip numbers with signature 0
        l -= 1
    if 0 < signature < 2048:  # Only process non-zero signatures
        # Make a copy of current DP state
        new_dp = dp.copy()
        # For each existing subset, calculate new subsets by adding current signature
        for existing in dp:
            new_dp[existing ^ signature] += dp[existing]
        dp = new_dp

# Calculate result
MOD = 1000000007
result = (dp[0] * mod_pow(2, l, MOD) - 1) % MOD
print(result)