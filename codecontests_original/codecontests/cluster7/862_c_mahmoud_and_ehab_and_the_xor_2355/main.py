#!/usr/bin/env python3

n, x = map(int, input().split())
if (n == 2 and x == 0):
    print("NO")
    quit()
a = 2**17
b = 2**18
ans = 0
print("YES")
if(n == 1):
    print(x)
    quit()
if (n == 2):
    print(x, 0)
    quit()
for i in range(n-3):
    print(i+1, end = " ")
    ans = (ans ^ (i+1))
if (ans == x):
    print(b, a, a+b)
else:
    print(0, a, a^ans^x)
