#!/usr/bin/env python3

from library import read_ints, create_dp_table
from collections import defaultdict

def main():
    # Read input
    n, l, k = read_ints()  # n tours, need to win l, can carry k prizes initially
    probabilities = read_ints()  # probability to win each tour (in percent)
    prizes = read_ints()  # prize type for each tour (-1 = huge prize, otherwise bag capacity)
    
    # Count number of huge prizes
    huge_prize_count = prizes.count(-1)
    
    # Convert probabilities to decimal
    probabilities = [p / 100 for p in probabilities]
    
    # Initialize DP state
    # states[(won_tours, bag_capacity)] = probability
    states = {(0, min(k, huge_prize_count)): 1.0}
    
    # Probability distribution of number of huge prizes won
    huge_prizes_won = [1.0]  # Initially, 0 huge prizes with probability 1
    
    # Process each tour
    for prob, prize in zip(probabilities, prizes):
        if prize > 0:  # We win a bag
            new_states = defaultdict(float)
            
            for (won_tours, bag_capacity), state_prob in states.items():
                # If we lose this tour
                new_states[(won_tours, bag_capacity)] += state_prob * (1 - prob)
                
                # If we win this tour
                new_won_tours = min(l, won_tours + 1)  # Cap at l, we only care if we reach l
                new_bag_capacity = min(huge_prize_count, bag_capacity + prize)  # Cap at max needed
                new_states[(new_won_tours, new_bag_capacity)] += state_prob * prob
            
            states = new_states
        else:  # We win a huge prize
            # Update the huge_prizes_won distribution
            new_distribution = [0] * (len(huge_prizes_won) + 1)
            
            # If we win a huge prize, we get one more
            for i, p in enumerate(huge_prizes_won):
                new_distribution[i] += p * (1 - prob)  # Don't win
                new_distribution[i+1] += p * prob  # Win
            
            huge_prizes_won = new_distribution
    
    # Initialize final probability table
    # dp[won_tours][huge_prizes] = probability
    dp = create_dp_table([n - huge_prize_count + 1, huge_prize_count + 1], 0.0)
    
    # Fill the table with successful states
    for (won_tours, bag_capacity), state_prob in states.items():
        # We need total wins >= l, and enough bag capacity for huge prizes
        if won_tours + bag_capacity >= l:
            dp[won_tours][bag_capacity] = state_prob
    
    # Process the DP table to get cumulative probabilities
    # First, accumulate probabilities for bag capacities
    for tours in range(n - huge_prize_count, -1, -1):
        for prizes in range(huge_prize_count, 0, -1):
            dp[tours][prizes-1] += dp[tours][prizes]
    
    # Then, accumulate probabilities for won tours
    for tours in range(n - huge_prize_count, 0, -1):
        for prizes in range(huge_prize_count, -1, -1):
            dp[tours-1][prizes] += dp[tours][prizes]
    
    # Calculate final answer
    result = 0.0
    for huge_prizes, prob in enumerate(huge_prizes_won):
        # Check if we can have a successful outcome with this many huge prizes
        if l - huge_prizes <= n - huge_prize_count:
            result += dp[max(0, l - huge_prizes)][huge_prizes] * prob
    
    # Handle potential small floating point errors by rounding very small values to 0
    if abs(result) < 1e-9:
        result = 0.0
    
    # Format output with 7 decimal places
    print(f"{result:.7f}")

if __name__ == "__main__":
    main()