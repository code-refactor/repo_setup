# Library Design Plan

Based on the analysis of the problems and solutions, I've identified common patterns and functions that would be beneficial to include in our library. This library focuses primarily on number theory functions, which appear to be the most common across the problems.

## Core Library Components

### 1. Number Theory Functions

#### Basic Operations
- `gcd(a, b)`: Calculate the greatest common divisor of two numbers
- `lcm(a, b)`: Calculate the least common multiple of two numbers
- `extended_gcd(a, b)`: Extended Euclidean algorithm to find coefficients x, y such that ax + by = gcd(a, b)
- `mod_inverse(a, m)`: Calculate the modular multiplicative inverse of a with respect to modulus m

#### Primality and Divisibility
- `is_prime(n)`: Check if a number is prime
- `find_divisors(n)`: Find all divisors of a number
- `count_divisors(n)`: Count the number of divisors of a number
- `prime_factorization(n)`: Get the prime factorization of a number
- `unique_prime_factors(n)`: Get the unique prime factors of a number
- `find_smallest_prime_factor(n)`: Find the smallest prime factor of a number

#### Advanced Number Theory
- `euler_totient(n)`: Calculate Euler's totient function φ(n)
- `legendre_formula(n, p)`: Count the highest power of prime p that divides n!
- `is_power_of_two_minus_one(n)`: Check if n is of the form 2^k - 1
- `find_first_k_factors(n, k)`: Find first k factors of n (excluding 1)
- `factor_counter(n)`: Return a Counter object with prime factors as keys and their powers as values

### 2. Modular Arithmetic

- `mod_pow(base, exp, mod)`: Calculate (base^exp) % mod efficiently
- `mod_add(a, b, mod)`: Calculate (a + b) % mod
- `mod_mul(a, b, mod)`: Calculate (a * b) % mod
- `mod_div(a, b, mod)`: Calculate (a / b) % mod (using modular inverse)

### 3. Utility Functions

- `arithmetic_series_sum(first, diff, terms)`: Calculate sum of arithmetic series
- `geometric_series_sum(first, ratio, terms)`: Calculate sum of geometric series
- `geometric_series_infinite_sum(first, ratio)`: Calculate sum of infinite geometric series

## Implementation Results

All the functions listed above have been implemented in the `library.py` file. The library provides a comprehensive set of number theory functions that have been used to refactor all the problem solutions in this cluster.

## Refactoring Checklist

All problems have been successfully refactored to use the library:

- [x] 1068_b_lcm_2510
- [x] 1076_b_divisor_subtraction_738
- [x] 1091_c_new_year_and_the_sphere_transmission_1262
- [x] 1110_c_meaningless_operations_3658
- [x] 1141_a_game_23_2618
- [x] 1228_c_primes_and_multiplication_13032
- [x] 1242_a_tile_painting_5747
- [x] 1243_c_tile_painting_2415
- [x] 1294_c_product_of_three_numbers_4292
- [x] 1295_d_same_gcds_6373
- [x] 1343_a_candies_8456
- [x] 1360_d_buying_shovels_6584
- [x] 1362_a_johnny_and_ancient_computer_1692
- [x] 1374_b_multiply_by_2_divide_by_6_231
- [x] 1444_a_division_6380
- [x] 1454_d_number_into_sequence_7733
- [x] 150_a_win_or_freeze_5134
- [x] 151_c_win_or_freeze_133
- [x] 177_b1_rectangular_game_2533
- [x] 271_e_three_horses_3683
- [x] 288_c_polo_the_penguin_and_xor_operation_9826
- [x] 371_b_fox_dividing_cheese_352
- [x] 487_c_prefix_product_sequence_2443
- [x] 576_a_vasya_and_petyas_game_7650
- [x] 680_c_bear_and_prime_100_4430
- [x] 762_a_kth_divisor_5057
- [x] 803_f_coprime_subsequences_8909
- [x] 893_e_counting_arrays_6936
- [x] 98_b_help_king_3609
- [x] 99_d_help_king_8501

## Key Improvements

1. **Code Reusability**: Common number theory functions are now shared across all problems
2. **Code Reduction**: Eliminated duplicated implementations of common algorithms
3. **Readability**: Solutions are now cleaner and focus on problem-specific logic
4. **Maintainability**: Changes to the library will automatically benefit all solutions
5. **Correctness**: All solutions pass their original tests
6. **Import Consistency**: Removed hardcoded import paths, relying on the run.sh scripts instead

## Summary

The library implementation successfully addresses the main objective of this task: to minimize the total amount of code needed to solve all problems. By identifying common patterns and creating reusable components, we've significantly reduced code duplication while maintaining correctness and improving readability. We've also removed unnecessary system path manipulation from all solutions, relying on the run.sh scripts to handle imports correctly.