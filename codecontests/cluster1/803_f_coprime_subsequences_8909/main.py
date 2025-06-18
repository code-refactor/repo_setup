#!/usr/bin/env python3

# 803F - Coprime Subsequences
from library import find_divisors
from collections import defaultdict

def solve():
    n = int(input())
    nums = list(map(int, input().split()))
    
    # Count how many numbers are divisible by each divisor
    count = defaultdict(int)
    for num in nums:
        divisors = find_divisors(num)
        for d in divisors:
            count[d] += 1
    
    if not count:
        return 0
        
    maxk = max(count.keys())
    
    # For each divisor d, calculate number of subsequences using numbers divisible by d
    # This is 2^count[d] - 1 (all non-empty subsets)
    freq = {k: (1 << count[k]) - 1 for k in count}
    
    # Use inclusion-exclusion principle to find subsequences with gcd exactly equal to k
    for k in sorted(count.keys(), reverse=True):
        for multiple in range(k * 2, maxk + 1, k):
            if multiple in freq:
                freq[k] -= freq[multiple]
    
    # Return number of subsequences with gcd = 1 (coprime subsequences)
    return freq[1] % (10**9 + 7)

print(solve())