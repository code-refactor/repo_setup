#!/usr/bin/env python3

def get_divisors(n):
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

# 803F
import collections

def do():
    n = int(input())
    nums = map(int, input().split(" "))
    count = collections.defaultdict(int)
    for num in nums:
        divisors = get_divisors(num)
        for d in divisors:
            count[d] += 1
    
    maxk = max(count.keys())
    freq = {k: (1 << count[k]) - 1 for k in count}
    for k in sorted(count.keys(), reverse=True):
        for kk in range(k << 1, maxk+1, k):
            freq[k] -= freq[kk] if kk in freq else 0
    return freq[1] % (10**9 + 7)

print(do())