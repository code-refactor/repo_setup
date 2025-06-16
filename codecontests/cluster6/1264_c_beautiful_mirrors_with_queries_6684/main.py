#!/usr/bin/env python3

from library import mod_inverse_general, MOD2

n, q = map(int, input().split())
p = list(map(int, input().split()))

checkpoints = [False] * (n + 1)
checkpoints[1] = True

def solve_expected():
    E = [0] * (n + 1)
    
    for i in range(n, 0, -1):
        if i == n:
            E[i] = 100 * mod_inverse_general(p[i-1], MOD2) % MOD2
        else:
            prob_success = p[i-1] * mod_inverse_general(100, MOD2) % MOD2
            prob_fail = (100 - p[i-1]) * mod_inverse_general(100, MOD2) % MOD2
            
            checkpoint_pos = i
            while checkpoint_pos > 0 and not checkpoints[checkpoint_pos]:
                checkpoint_pos -= 1
            
            expected_val = (1 + prob_success * E[i+1] + prob_fail * E[checkpoint_pos]) % MOD2
            E[i] = expected_val * mod_inverse_general(prob_success, MOD2) % MOD2
    
    return E[1]

for _ in range(q):
    u = int(input())
    checkpoints[u] = not checkpoints[u]
    print(solve_expected())