#!/usr/bin/env python3

import os
import sys
from library import MOD2, mod_inverse
input = sys.stdin.buffer.readline
#sys.setrecursionlimit(int(2e5)) 
from collections import deque
import math
#  list(map(int, input().split()))
#####################################################################################

class CF(object):
    def __init__(self):
        self.mod = MOD2
        self.n = int(input())
        self.a = list(map(int, input().split()))
        self.tot = sum(self.a)
        self.dp = [[0,0] for _ in range(self.tot+1)]

    def inv(self, x):
        return mod_inverse(x, self.mod)

    def gao(self):
        self.dp[0] = [0,1]
        self.dp[1] = [(1-self.n+self.mod)%self.mod, 1]
        for k in range(1, self.tot):
            temp = self.inv(self.tot-k)
            self.dp[k+1][0] = -self.tot*(self.n - 1) - self.dp[k][0] * (2*k - self.tot- k*self.n) - self.dp[k-1][0] *k*(self.n-1)
            self.dp[k+1][0] *= temp
            self.dp[k+1][0] = (self.dp[k+1][0] %self.mod+self.mod)%self.mod            
            self.dp[k+1][1] = -self.dp[k][1]*(2*k - self.tot- k*self.n) - self.dp[k-1][1]*k*(self.n-1)
            self.dp[k+1][1] *= temp
            self.dp[k+1][1] = (self.dp[k+1][1] %self.mod+self.mod)%self.mod
        
        alpha = -self.dp[self.tot][0]*self.inv(self.dp[self.tot][1])
        alpha = (alpha%self.mod + self.mod)%self.mod
        #print(alpha)
        ans=0
        for i in range(self.n):
            ans += self.dp[self.a[i]][0] + self.dp[self.a[i]][1] * alpha
            ans = (ans%self.mod+self.mod)%self.mod
        ans -= alpha * (self.n - 1)
        ans = (ans%self.mod+self.mod)%self.mod
        ans *= self.inv(self.n)
        ans = (ans%self.mod+self.mod)%self.mod
        print(ans)


    def main(self):            
        self.gao()
        pass

if __name__ == "__main__":
    cf = CF()
    cf.main()
    pass

'''
dp[k+1] *(tot-k) = -tot*(n-1) - dp[k]*(2*k - tot- k*n ) - dp[k-1] *k*(n-1)

'''