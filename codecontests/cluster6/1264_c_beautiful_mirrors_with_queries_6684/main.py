#!/usr/bin/env python3

from library import MOD2, mod_inverse

def solve_beautiful_mirrors():
    # Read input
    line1 = input().split()
    N = int(line1[0])
    q = int(line1[1])
    A = list(map(int, input().split()))
    
    # Initially only mirror 1 is a checkpoint
    checkpoints = {1}
    
    # Process each query
    for _ in range(q):
        u = int(input())
        
        # Toggle checkpoint status
        if u in checkpoints:
            checkpoints.remove(u)
        else:
            checkpoints.add(u)
        
        # Calculate expected value
        K = 0
        P = 0
        Q = 1
        
        for i, a in enumerate(A):
            # Convert probabilities to fractions
            p0 = (a * mod_inverse(100, MOD2)) % MOD2
            q0 = ((100-a) * mod_inverse(100, MOD2)) % MOD2
            
            # If this is a checkpoint, update values
            if i+1 in checkpoints:
                P = (P + (i+1)*Q*q0) % MOD2
                K = (K + Q*q0) % MOD2
            
            # Update probability of continuing
            Q = (Q * p0) % MOD2
        
        # Calculate final result
        inv = (MOD2 + 1 - K) % MOD2
        w = (N*Q + P) % MOD2
        ans = (w * mod_inverse(inv, MOD2)) % MOD2
        print(ans)

if __name__ == "__main__":
    solve_beautiful_mirrors()