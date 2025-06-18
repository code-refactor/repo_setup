#!/usr/bin/env python3

from library import read_int, read_ints, factorial, create_dp_table

def solve_maxim_restaurant():
    # Read input
    n = read_int()
    guest_sizes = read_ints()
    table_length = read_int()
    
    # Check if all guests fit at the table
    total_size = sum(guest_sizes)
    if total_size <= table_length:
        return n
    
    # Calculate the expected number of guests
    expected_guests = 0
    
    # Try each guest as the one who doesn't fit
    for i in range(n):
        # Initialize DP array
        # dp[j][k][z] = number of ways to arrange j guests with k of them at the table
        # and their total size is z
        dp = [[[0 for _ in range(table_length + 1)] for _ in range(n + 1)] for _ in range(n)]
        
        # Base case: before considering any guests, there are 0 guests with total size 0
        dp[-1][0][0] = 1
        
        # Fill DP table
        for j in range(n):
            if j == i:
                # Skip the guest who doesn't fit
                for k in range(n):
                    for z in range(table_length + 1):
                        dp[j][k][z] = dp[j-1][k][z]
                continue
            
            for k in range(n):
                for z in range(table_length + 1):
                    # Option 1: Don't take this guest
                    dp[j][k][z] += dp[j-1][k][z]
                    
                    # Option 2: Take this guest if there's enough space
                    if z + guest_sizes[j] <= table_length:
                        dp[j][k+1][z + guest_sizes[j]] += dp[j-1][k][z]
        
        # Calculate contribution to expected value
        for k in range(n):
            for z in range(table_length + 1):
                if z + guest_sizes[i] > table_length:
                    # If adding guest i would exceed table length
                    # This accounts for a valid arrangement where k guests are served
                    # and guest i is the first one who doesn't fit
                    arrangements = dp[n-1][k][z] * factorial(k) * factorial(n-k-1)
                    expected_guests += k * arrangements
    
    # Divide by total number of possible arrangements
    return expected_guests / factorial(n)

def main():
    result = solve_maxim_restaurant()
    print(f"{result:.10f}")

if __name__ == "__main__":
    main()
