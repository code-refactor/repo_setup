#!/usr/bin/env python3

def get_divisors(n):
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

n=int(input())
a = get_divisors(n)
ans=[]
for i in a:
    term=n//i
    ans.append((term*(2+(term-1)*i))//2)
ans.sort()
print(*ans)