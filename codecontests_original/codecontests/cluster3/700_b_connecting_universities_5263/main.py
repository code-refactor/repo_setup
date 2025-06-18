#!/usr/bin/env python3

def bfs(source):

    q = [0] * (n + 1);

    fa = [-1] * n

    l, r = [1] * 2

    fa[source] = source

    q[1] = source

    while l <= r:

        x = q[l]

        l += 1

        for y in e[x]:

            if  fa[y] == -1:

                fa[y] = x

                r += 1

                q[r] = y

    i = r;

    while i >= 1:

        x = q[i]

        for y in e[x]:

            if fa[y] == x:

                sum[x] += sum[y]

                dp[x] += dp[y] + min(sum[y], m - sum[y])

        i -= 1



n, m =[int(x) for x in input().split()]

m <<= 1

t = [int(x) for x in input().split()]

e = [list() for i in range(n)]

sum = [0] * n

dp = [0] * n

#print(len(e), e)

for i in range(n - 1):

    x, y = [int(a) for a in input().split()]

    e[x - 1].append(y - 1)

    e[y - 1].append(x - 1)

for x in t:

    sum[x - 1] = 1

bfs(0)

print(dp[0])



# Made By Mostafa_Khaled