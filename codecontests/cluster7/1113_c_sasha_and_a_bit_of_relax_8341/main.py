#!/usr/bin/env python3

from library import read_int, read_array, xor_prefix

n = read_int()
a = read_array()

# Get XOR prefix array
pref = xor_prefix(a)

# Initialize counters for prefix XORs by parity (even/odd position)
dp = [[0 for _ in range(2**20 + 5)] for _ in range(2)]
ans = 0

# Count segments where XOR is 0
for i in range(len(pref)):
    ans += dp[i % 2][pref[i]]
    dp[i % 2][pref[i]] += 1
    
print(ans)