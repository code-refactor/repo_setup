#!/usr/bin/env python3

from library import read_int, read_ints, mod_add, mod_mul, mod_pow, mod_inverse, MOD1

def calculate_probability(l_arr, r_arr):
    """
    Calculate the probability that adjacent elements are different
    """
    # Find the maximum lower bound and minimum upper bound
    l_max, r_min = max(l_arr), min(r_arr)
    
    # If there's no overlap in ranges, probability is 1
    if l_max > r_min:
        return 1
    
    # Calculate intersection probability
    p = (r_min - l_max + 1)
    for l, r in zip(l_arr, r_arr):
        p = mod_mul(p, mod_inverse(r - l + 1, MOD1), MOD1)
    
    # Return probability of being different
    return (1 - p) % MOD1

def main():
    # Read input
    n = read_int()
    L = read_ints()  # Lower bounds
    R = read_ints()  # Upper bounds
    
    # Initialize variables for expected values
    EX = 0   # Expected value of B(x)
    EX2 = 0  # Expected value of B(x)^2
    P = [0] * n  # Probability of cut at position i
    pre = [0] * n  # Prefix sum of probabilities
    
    # Calculate probabilities and expectations
    for i in range(1, n):
        # Probability that adjacent elements i-1 and i are different
        P[i] = calculate_probability(L[i-1:i+1], R[i-1:i+1])
        
        # Update prefix sum
        pre[i] = mod_add(pre[i-1], P[i], MOD1)
        
        # Handle three consecutive elements
        if i >= 2:
            # Probabilities of different events
            pA = 1 - P[i-1]  # Probability that elements i-2 and i-1 are same
            pB = 1 - P[i]    # Probability that elements i-1 and i are same
            pAB = 1 - calculate_probability(L[i-2:i+1], R[i-2:i+1])  # Probability that i-2, i-1, i are all same
            
            # Probability of exactly one cut between three elements
            p_ = 1 - (pA + pB - pAB)
            
            # Update E[B(x)^2] calculation
            term = mod_add(mod_mul(P[i], pre[i-2], MOD1), p_, MOD1)
            EX2 = mod_add(EX2, mod_mul(2, term, MOD1), MOD1)
    
    # Calculate final expected values
    EX = sum(P) % MOD1
    EX2 = mod_add(EX2, EX, MOD1)
    
    # Final answer: E[B(x)^2 + 2B(x) + 1] = E[B(x) + 1]^2
    ans = mod_add(mod_add(EX2, mod_mul(2, EX, MOD1), MOD1), 1, MOD1)
    print(ans)

if __name__ == "__main__":
    main()