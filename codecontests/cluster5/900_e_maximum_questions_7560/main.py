#!/usr/bin/env python3

from itertools import accumulate

n = int(input())
s = input()
m = int(input())

# Prefix sums for 'a', 'b', and '?'
b_count = [0] * (n + 2)
a_count = [0] * (n + 2)
q_count = list(accumulate([0] + [c == '?' for c in s]))

for i in range(n):
    b_count[i] = b_count[i - 2] + (s[i] == 'b')
    a_count[i] = a_count[i - 2] + (s[i] == 'a')

# Dynamic programming
dp = [(0, 0)] * (n + 2)

for i in range(n - m, -1, -1):
    dp[i] = dp[i + 1]
    
    b_check_idx = 1 if m % 2 == 1 else 2
    a_check_idx = 1 if m % 2 == 0 else 2
    
    # Check if segment can be made alternating
    has_b = b_count[i + m - b_check_idx] - b_count[i - 2]
    has_a = a_count[i + m - a_check_idx] - a_count[i - 1]
    
    if not (has_b or has_a):
        cost, questions = dp[i + m]
        new_questions = questions + q_count[i + m] - q_count[i]
        dp[i] = min((cost - 1, new_questions), dp[i])

print(dp[0][1])

