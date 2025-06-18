# 285_E. Positions in Permutations

**ID:** 285_e_positions_in_permutations_13052
**Difficulty:** 11

## Description

Permutation p is an ordered set of integers p1, p2, ..., pn, consisting of n distinct positive integers, each of them doesn't exceed n. We'll denote the i-th element of permutation p as pi. We'll call number n the size or the length of permutation p1, p2, ..., pn.

We'll call position i (1 ≤ i ≤ n) in permutation p1, p2, ..., pn good, if |p[i] - i| = 1. Count the number of permutations of size n with exactly k good positions. Print the answer modulo 1000000007 (109 + 7).

Input

The single line contains two space-separated integers n and k (1 ≤ n ≤ 1000, 0 ≤ k ≤ n).

Output

Print the number of permutations of length n with exactly k good positions modulo 1000000007 (109 + 7).

Examples

Input

1 0


Output

1


Input

2 1


Output

0


Input

3 2


Output

4


Input

4 1


Output

6


Input

7 4


Output

328

Note

The only permutation of size 1 has 0 good positions.

Permutation (1, 2) has 0 good positions, and permutation (2, 1) has 2 positions.

Permutations of size 3:

  1. (1, 2, 3) — 0 positions
  2. <image> — 2 positions
  3. <image> — 2 positions
  4. <image> — 2 positions
  5. <image> — 2 positions
  6. (3, 2, 1) — 0 positions

## Categories

- combinatorics
- dp
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 1
```

**Output**:
```
0
```

### Example 2

**Input**:
```
4 1
```

**Output**:
```
6
```

### Example 3

**Input**:
```
7 4
```

**Output**:
```
328
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
