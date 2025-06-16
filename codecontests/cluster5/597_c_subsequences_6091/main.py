#!/usr/bin/env python3

from library import FenwickTree

def main():
    n,k = map(int,input().split())
    arr = [int(input()) for _ in range(n)]
    dp = [[0]*n for _ in range(k+1)]
    dp[0] = [1]*n
    for i in range(1,k+1):
        tree = FenwickTree(n)
        for j in range(n):
            dp[i][j] = tree.query(arr[j]-1)
            tree.update(arr[j], dp[i-1][j])
    print(sum(dp[-1]))

if __name__ == '__main__':
    main()