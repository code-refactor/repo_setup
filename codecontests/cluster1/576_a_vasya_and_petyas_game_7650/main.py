#!/usr/bin/env python3

def prime_factorize(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    if n > 2:
        factors.append(n)
    return factors

def input_ints():
    return list(map(int, input().split()))

def main():
    n = int(input())
    ans = []
    
    # Group by prime base
    primes_used = set()
    
    for x in range(2, n + 1):
        factors = prime_factorize(x)
        # Check if all factors are the same (i.e., x is a prime power)
        if len(set(factors)) == 1:
            primes_used.add(factors[0])
    
    # Output all powers of each prime in order
    for prime in sorted(primes_used):
        power = prime
        while power <= n:
            ans.append(power)
            power *= prime
    
    print(len(ans))
    print(' '.join(str(x) for x in ans))

if __name__ == '__main__':
    main()
