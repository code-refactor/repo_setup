from library import *

n = int_inp()
t = list(ints())

p, s, r = [0] * n, [0] * n, t[0]

for i in range(n - 1):
    j = i + 1
    x = t[j]
    
    if x > r:
        r = x
    else:
        while t[i] < x:
            s[j], i = max(s[j], s[i]), p[i]
        p[j] = i
        s[j] += 1

print(max(s))