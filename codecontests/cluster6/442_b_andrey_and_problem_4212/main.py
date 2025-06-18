#!/usr/bin/env python3

from library import read_int, read_floats

def solve_andrey_problem():
    # Read input
    n = read_int()
    probabilities = read_floats()
    
    # Sort probabilities in descending order
    probabilities.sort(reverse=True)
    
    # Special case: if any probability is 1, the answer is 1
    if max(probabilities) == 1:
        return 1
    
    # Update n to be the actual length of probabilities
    n = len(probabilities)
    
    # Pre-compute the product of (1-p_i) for optimization
    # pre[i] = product of (1-p_j) for j from 0 to i
    pre = [1] * 100
    pre[0] = 1 - probabilities[0]
    for i in range(1, n):
        pre[i] = pre[i-1] * (1 - probabilities[i])
    
    # Try all possible number of friends to ask
    best_probability = 0
    for i in range(1, n+1):
        # Calculate probability of getting exactly one problem
        # from the first i friends
        current_probability = 0
        for j in range(i):
            # P(friend j submits) * P(no other friend in the set submits)
            current_probability += pre[i-1] / (1 - probabilities[j]) * probabilities[j]
        
        best_probability = max(best_probability, current_probability)
    
    return best_probability

def main():
    result = solve_andrey_problem()
    print('%.10f' % result)

if __name__ == "__main__":
    main()