#!/usr/bin/env python3

n = int(input()); s = input(); m = int(input())
a = [0]*(n+2); b = [0]*(n+2); q = [0]*(n+1);
dp = [(0, 0)]*(n+2)

for i in range(0, n):
  b[i] = b[i-2]+(s[i] == 'b')
  a[i] = a[i-2]+(s[i] == 'a')
  q[i] = q[i-1]+(s[i] == '?')
  
for i in range(n-m, -1, -1):
  dp[i] = dp[i+1]
  i_b = 1 if m%2 == 1 else 2
  i_a = 1 if m%2 == 0 else 2
  
  if not (b[i+m-i_b]-b[i-2] or a[i+m-i_a]-a[i-1]):
    t, r = dp[i+m]
    dp[i] = min((t-1, r+q[i+m-1]-q[i-1]), dp[i])
print(dp[0][1])

