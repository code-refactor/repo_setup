# 1228_C. Primes and Multiplication

**ID:** 1228_c_primes_and_multiplication_13032
**Difficulty:** 9

## Description

Let's introduce some definitions that will be needed later.

Let prime(x) be the set of prime divisors of x. For example, prime(140) = \{ 2, 5, 7 \}, prime(169) = \{ 13 \}.

Let g(x, p) be the maximum possible integer p^k where k is an integer such that x is divisible by p^k. For example:

  * g(45, 3) = 9 (45 is divisible by 3^2=9 but not divisible by 3^3=27), 
  * g(63, 7) = 7 (63 is divisible by 7^1=7 but not divisible by 7^2=49). 



Let f(x, y) be the product of g(y, p) for all p in prime(x). For example:

  * f(30, 70) = g(70, 2) ⋅ g(70, 3) ⋅ g(70, 5) = 2^1 ⋅ 3^0 ⋅ 5^1 = 10, 
  * f(525, 63) = g(63, 3) ⋅ g(63, 5) ⋅ g(63, 7) = 3^2 ⋅ 5^0 ⋅ 7^1 = 63. 



You have integers x and n. Calculate f(x, 1) ⋅ f(x, 2) ⋅ … ⋅ f(x, n) mod{(10^{9} + 7)}.

Input

The only line contains integers x and n (2 ≤ x ≤ 10^{9}, 1 ≤ n ≤ 10^{18}) — the numbers used in formula.

Output

Print the answer.

Examples

Input


10 2


Output


2


Input


20190929 1605


Output


363165664


Input


947 987654321987654321


Output


593574252

Note

In the first example, f(10, 1) = g(1, 2) ⋅ g(1, 5) = 1, f(10, 2) = g(2, 2) ⋅ g(2, 5) = 2.

In the second example, actual value of formula is approximately 1.597 ⋅ 10^{171}. Make sure you print the answer modulo (10^{9} + 7).

In the third example, be careful about overflow issue.

## Categories

- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
20190929 1605
```

**Output**:
```
363165664
```

### Example 2

**Input**:
```
10 2
```

**Output**:
```
2
```

### Example 3

**Input**:
```
947 987654321987654321
```

**Output**:
```
593574252
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
