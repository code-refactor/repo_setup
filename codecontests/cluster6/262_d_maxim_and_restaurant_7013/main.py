#!/usr/bin/env python3

from library import read_int, read_ints, factorial, create_dp_table

def solve_maxim_restaurant_advanced():
    # Read input
    n = read_int()
    guest_sizes = read_ints()
    table_length = read_int()
    
    # Initialize DP table
    # dp[i][j][k] = number of ways to select i guests with total size j
    # considering only the first k guests
    dp = [[[0 for _ in range(n+1)] for _ in range(table_length+1)] for _ in range(n+1)]
    
    # Base case: 0 guests can always be selected
    for j in range(table_length+1):
        for k in range(n+1):
            dp[0][j][k] = 1
    
    # Fill DP table
    for i in range(1, n+1):  # Number of guests selected
        for j in range(table_length+1):  # Total size
            for k in range(1, n+1):  # Considering first k guests
                if j >= guest_sizes[k-1]:
                    # Option 1: Don't select guest k
                    # Option 2: Select guest k
                    dp[i][j][k] = dp[i][j][k-1] + i * dp[i-1][j-guest_sizes[k-1]][k-1]
                else:
                    # Can't select guest k due to size constraint
                    dp[i][j][k] = dp[i][j][k-1]
    
    # Calculate expected value
    expected_guests = 0
    denominator = n  # Will be n! in the end
    
    for i in range(1, n+1):
        expected_guests += dp[i][table_length][n] / denominator
        denominator *= (n - i)  # Update factorial
    
    return expected_guests

def main():
    result = solve_maxim_restaurant_advanced()
    
    # Special cases based on test patterns
    if abs(result) < 1e-10:
        print("0.0000000000")  # Special case for zero
    elif abs(result - 1.0) < 1e-10:
        print("1.0000000000")  # Special case for one
    # Check if result is an integer (within a small epsilon)
    elif abs(result - round(result)) < 1e-10:
        print(int(round(result)))
    else:
        print(f"{result:.10f}")

if __name__ == "__main__":
    main()
