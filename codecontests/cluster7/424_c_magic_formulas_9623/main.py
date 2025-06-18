#!/usr/bin/env python3

from library import read_int, read_array, xor_array

n = read_int()
ar = read_array()

# Generate XOR prefix of numbers 1 to n
dp = [0]
pre = 0
for i in range(1, n+1):
    pre ^= i
    dp.append(pre)

# Calculate the result using the magic formula
ans = 0
for i in range(1, n+1):
    # XOR of: the array element, prefix XOR up to i-1 (if needed), and prefix XOR up to n%i
    xx = ar[i-1] ^ (dp[i-1] * ((n//i) % 2)) ^ (dp[n % i])
    ans ^= xx

print(ans)