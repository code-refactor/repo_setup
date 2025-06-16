#!/usr/bin/env python3

n, q = map(int, input().split())
rules = {}
for _ in range(q):
    from_str, to_char = input().split()
    rules[from_str] = to_char

# dp[length][char] = number of strings of given length ending with char that can compress to 'a'
dp = [[0] * 6 for _ in range(n + 1)]
chars = "abcdef"

# Base case: strings of length 1 that can compress to 'a'
dp[1][0] = 1  # Only 'a' itself

# Fill the DP table
for length in range(2, n + 1):
    for c1 in range(6):  # first character
        for c2 in range(6):  # second character
            two_char = chars[c1] + chars[c2]
            if two_char in rules:
                # This two-character string can be compressed
                result_char = rules[two_char]
                result_idx = chars.index(result_char)
                # Add the number of ways to compress strings of length (length-1) ending with result_char
                dp[length][c1] += dp[length - 1][result_idx]

print(sum(dp[n]))