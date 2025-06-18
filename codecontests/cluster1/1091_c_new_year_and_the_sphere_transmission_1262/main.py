#!/usr/bin/env python3
from library import find_divisors, arithmetic_series_sum

n = int(input())

# Get all divisors of n
divisors = find_divisors(n)

# Calculate the fun values for each divisor
fun_values = []
for k in divisors:
    # Number of terms in the sequence
    term = n // k
    
    # For step size k, the sequence is 1, 1+k, 1+2k, ..., 1+(term-1)*k
    # We use the arithmetic series sum formula: n/2 * (2a + (n-1)d)
    # Where a is the first term (1), d is the common difference (k), and n is the number of terms (term)
    fun_value = arithmetic_series_sum(1, k, term)
    fun_values.append(fun_value)

# Sort and print the fun values
fun_values.sort()
print(*fun_values)