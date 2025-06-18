# 1174_E. Ehab and the Expected GCD Problem

**ID:** 1174_e_ehab_and_the_expected_gcd_problem_6367
**Difficulty:** 11

## Description

Let's define a function f(p) on a permutation p as follows. Let g_i be the [greatest common divisor (GCD)](https://en.wikipedia.org/wiki/Greatest_common_divisor) of elements p_1, p_2, ..., p_i (in other words, it is the GCD of the prefix of length i). Then f(p) is the number of distinct elements among g_1, g_2, ..., g_n.

Let f_{max}(n) be the maximum value of f(p) among all permutations p of integers 1, 2, ..., n.

Given an integers n, count the number of permutations p of integers 1, 2, ..., n, such that f(p) is equal to f_{max}(n). Since the answer may be large, print the remainder of its division by 1000 000 007 = 10^9 + 7.

Input

The only line contains the integer n (2 ≤ n ≤ 10^6) — the length of the permutations.

Output

The only line should contain your answer modulo 10^9+7.

Examples

Input


2


Output


1

Input


3


Output


4

Input


6


Output


120

Note

Consider the second example: these are the permutations of length 3:

  * [1,2,3], f(p)=1. 
  * [1,3,2], f(p)=1. 
  * [2,1,3], f(p)=2. 
  * [2,3,1], f(p)=2. 
  * [3,1,2], f(p)=2. 
  * [3,2,1], f(p)=2. 



The maximum value f_{max}(3) = 2, and there are 4 permutations p such that f(p)=2.

## Categories

- combinatorics
- dp
- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
```

**Output**:
```
1
```

### Example 2

**Input**:
```
3
```

**Output**:
```
4
```

### Example 3

**Input**:
```
6
```

**Output**:
```
120
```


## Testing

Run the solution with:

```bash
./run.sh
```

Or test with a specific input file:

```bash
uv run main.py < tests/input_1.txt
```
