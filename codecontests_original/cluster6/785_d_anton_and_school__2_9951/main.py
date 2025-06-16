#!/usr/bin/env python3

mod = 10 ** 9 + 7

fact, inv, invfact = [1, 1], [0, 1], [1, 1]
for i in range(2, 200200):
    fact.append(fact[-1] * i % mod)
    inv.append(inv[mod % i] * (mod - mod // i) % mod)
    invfact.append(invfact[-1] * inv[-1] % mod)

def C(n, k):
    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] * invfact[n - k] % mod

s = input()
op, cl = 0, s.count(')')
ans = 0
for x in s:
    if x == '(':
        op += 1
        cur = C(cl + op - 1, op)
        ans += cur
    else:
        cl -= 1

print(ans % mod)
