#!/usr/bin/env python3

def sum(x):
    ans = 0
    for i in x:
        ans ^= i
    return ans

i = lambda: [*map(int, input().split())]
n, m = i()
a = i()
b = i()
if sum(a) != sum(b):
    print("NO")
    quit()
print("YES")
one = sum(a[1:]) ^ b[0]
print(one, end = " ")
for i in b[1:]:
    print(i, end = " ")
print()
st = ""
for i in range(m - 1):
    st += "0 "
for i in a[1:]:
    print(i, end = " ")
    print(st)

