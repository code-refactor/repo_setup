#!/usr/bin/env python3

from library import read_str, read_int, read_strs, mod_add, mod_sub, mod_mul, mod_pow, MOD1
import sys

def solve_colony_problem():
    s = read_str()
    n = len(s)
    
    # Map characters to indices (a-z: 0-25, A-Z: 26-51)
    def char_to_index(c):
        if 'A' <= c <= 'Z':
            return ord(c) - ord('A') + 26
        else:
            return ord(c) - ord('a')
    
    # Count frequency of each character
    char_counts = [0] * 101
    for char in s:
        char_counts[char_to_index(char)] += 1
    
    # Precompute factorials and inverses
    fac = [0] * (n + 1)
    inv = [0] * (n + 1)
    
    fac[0] = 1
    for i in range(1, n + 1):
        fac[i] = mod_mul(fac[i - 1], i, MOD1)
    
    inv[n] = mod_pow(fac[n], MOD1 - 2, MOD1)
    for i in range(n - 1, -1, -1):
        inv[i] = mod_mul(inv[i + 1], (i + 1), MOD1)
    
    # Calculate base number of arrangements
    num = mod_pow(fac[n // 2], 2, MOD1)
    for i in range(52):
        num = mod_mul(num, inv[char_counts[i]], MOD1)
    
    # Initialize DP array
    dp = [0] * (n + 1)
    dp[0] = 1
    
    # Fill DP array
    for i in range(52):
        if not char_counts[i]:
            continue
        for j in range(n, char_counts[i] - 1, -1):
            dp[j] = mod_add(dp[j], dp[j - char_counts[i]], MOD1)
    
    # Calculate answer for each pair
    ans = [[0] * 55 for _ in range(55)]
    for i in range(52):
        ans[i][i] = dp[n // 2]
    
    for i in range(52):
        if not char_counts[i]:
            continue
        temp_dp = dp.copy()
        
        for k in range(char_counts[i], n + 1):
            temp_dp[k] = mod_sub(temp_dp[k], temp_dp[k - char_counts[i]], MOD1)
        
        for j in range(i + 1, 52):
            if not char_counts[j]:
                continue
            
            for k in range(char_counts[j], n + 1):
                temp_dp[k] = mod_sub(temp_dp[k], temp_dp[k - char_counts[j]], MOD1)
            
            ans[i][j] = mod_mul(2, temp_dp[n // 2], MOD1)
            
            for k in range(n, char_counts[j] - 1, -1):
                temp_dp[k] = mod_add(temp_dp[k], temp_dp[k - char_counts[j]], MOD1)
    
    # Process queries
    q = read_int()
    queries = []
    for _ in range(q):
        line = input().split()
        x, y = int(line[0]), int(line[1])
        l, r = char_to_index(s[x - 1]), char_to_index(s[y - 1])
        if l > r:
            l, r = r, l
        print(mod_mul(num, ans[l][r], MOD1))

if __name__ == "__main__":
    solve_colony_problem()
