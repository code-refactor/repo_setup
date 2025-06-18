#!/usr/bin/env python3

from library import read_strs, create_dp_table

def main():
    n_str, p_str, t_str = read_strs()
    n = int(n_str)
    p = float(p_str)
    t = int(t_str)
    
    # Simple edge cases
    if p == 0:
        print("0.000000000000")
        return
    if p == 1:
        print(f"{min(n, t)}.000000000000")
        return
    if n >= t:
        print(f"{t * p:.12f}")
        return
    
    # Create DP table
    # dp[i][j] = probability that after i seconds, j people are on the escalator
    dp = create_dp_table([t+1, n+1], 0.0)
    dp[0][0] = 1.0  # Base case: at time 0, 0 people are on the escalator with 100% probability
    
    # Fill the DP table
    for i in range(t):
        for j in range(min(i+1, n)+1):
            if j < n:
                # Person enters the escalator with probability p
                dp[i+1][j+1] += dp[i][j] * p
                # Person doesn't enter with probability (1-p)
                dp[i+1][j] += dp[i][j] * (1 - p)
            else:
                # Already n people on the escalator, no more can enter
                dp[i+1][j] += dp[i][j]
    
    # Calculate expected value
    expected = sum(j * dp[t][j] for j in range(n+1))
    print(f"{expected:.12f}")

if __name__ == "__main__":
    main()
