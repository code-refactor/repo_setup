#!/usr/bin/env python3

from library import z_function, read_str

s = read_str()
n = len(s)
Z = z_function(s)

third = []
for i in range(n):
    if i + Z[i] == n:
        third.append(Z[i])
ll = len(third)

ans = ""
if ll == 0:
    ans = 'Just a legend'
elif ll == 1:
    if Z.count(third[0]) >= 2 or max(Z) > third[0]:
        ans = s[:third[0]]
    else:
        ans = 'Just a legend'
else:
    if Z.count(third[0]) >= 2 or max(Z) > third[0]:
        ans = s[:third[0]]
    else:
        ans = s[:third[1]]
print(ans)