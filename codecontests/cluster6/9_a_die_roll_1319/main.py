#!/usr/bin/env python3

from library import read_strs, reduce_fraction

def main():
    x, y = read_strs()
    x, y = int(x), int(y)
    
    # Calculate favorable outcomes
    favorable_outcomes = 7 - max(x, y)
    total_outcomes = 6
    
    # Reduce the fraction
    num, den = reduce_fraction(favorable_outcomes, total_outcomes)
    
    # Print the result
    print(f"{num}/{den}")

if __name__ == "__main__":
    main()

