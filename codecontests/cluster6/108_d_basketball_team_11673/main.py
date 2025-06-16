#!/usr/bin/env python3

from library import Combinatorics

n, m, h = map(int, input().split())
arr = list(map(int, input().split()))

total = sum(arr)

if total < n:
    print("-1")
    exit()

comb = Combinatorics(total, use_mod=False)

total_ways = comb.C(total - 1, n - 1)
same_dept = arr[h - 1] - 1
other_dept = total - arr[h - 1]

if same_dept == 0:
    prob_no_teammate = 1.0
else:
    prob_no_teammate = comb.C(other_dept, n - 1) / total_ways

prob_at_least_one = 1.0 - prob_no_teammate
print("{0:.10f}".format(prob_at_least_one))
