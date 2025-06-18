#!/usr/bin/env python3

from library import read_ints, read_array, xor_prefix, count_frequency

n, k = read_ints()
arr = read_array()

# Calculate XOR prefix array
pref = xor_prefix(arr)

# Group prefix XORs by their minimum and maximum XOR with (2^k-1)
dic = {}
for num in pref:
    # Get equivalent values under XOR with (2^k-1)
    complement = (2**k - 1) ^ num
    x = (min(num, complement), max(num, complement))
    
    if x in dic:
        dic[x] += 1
    else:
        dic[x] = 1

# Calculate number of valid segments
ans = 0
for elem in dic:
    m = dic[elem]
    # Count pairs of same value
    half = m // 2
    ans += half * (half - 1) / 2
    half = m - half
    ans += half * (half - 1) / 2

# Total possible segments minus invalid segments
ans = n * (n + 1) / 2 - ans
print(int(ans))