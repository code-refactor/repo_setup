#!/usr/bin/env python3

# 803F
import math
import collections
def do():
    n = int(input())
    nums = map(int, input().split(" "))
    count = collections.defaultdict(int)
    for num in nums:
        for i in range(1, int(math.sqrt(num))+1):
            cp = num // i
            if num % i == 0:
                count[i] += 1
            if cp != i and num % cp == 0:
                count[cp] += 1
    maxk = max(count.keys())
    freq = {k: (1 << count[k]) - 1 for k in count}
    for k in sorted(count.keys(), reverse=True):
        for kk in range(k << 1, maxk+1, k):
            freq[k] -= freq[kk] if kk in freq else 0
    return freq[1] % (10**9 + 7)

print(do())