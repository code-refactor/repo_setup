#!/usr/bin/env python3

def main():
    from sys import stdin
    input = stdin.readline
    # input = open('25-B.txt', 'r').readline

    n, k = map(int, input().split())
    s = input()[:-1]
    dp = [[0] * 26 for i in range(n + 1)]
    dp[0][0] = 1
    for ch in s:
        j = ord(ch) - ord('a')
        for i in range(n, 0, -1):
            dp[i][j] = sum(dp[i - 1])
    x = 0
    y = 0
    for i in range(n, -1, -1):
        if x + sum(dp[i]) >= k:
            print(k * n - y - (k - x) * i)
            break
        x += sum(dp[i])
        y += i * sum(dp[i])
    else:
        print(-1)
    
main()
