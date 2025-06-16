# 397_C. On Number of Decompositions into Multipliers

**ID:** 397_c_on_number_of_decompositions_into_multipliers_6811
**Difficulty:** 9

## Description

You are given an integer m as a product of integers a1, a2, ... an <image>. Your task is to find the number of distinct decompositions of number m into the product of n ordered positive integers.

Decomposition into n products, given in the input, must also be considered in the answer. As the answer can be very large, print it modulo 1000000007 (109 + 7).

Input

The first line contains positive integer n (1 ≤ n ≤ 500). The second line contains space-separated integers a1, a2, ..., an (1 ≤ ai ≤ 109).

Output

In a single line print a single number k — the number of distinct decompositions of number m into n ordered multipliers modulo 1000000007 (109 + 7).

Examples

Input

1
15


Output

1


Input

3
1 1 2


Output

3


Input

2
5 7


Output

4

Note

In the second sample, the get a decomposition of number 2, you need any one number out of three to equal 2, and the rest to equal 1.

In the third sample, the possible ways of decomposing into ordered multipliers are [7,5], [5,7], [1,35], [35,1].

A decomposition of positive integer m into n ordered multipliers is a cortege of positive integers b = {b1, b2, ... bn} such that <image>. Two decompositions b and c are considered different, if there exists index i such that bi ≠ ci.

## Categories

- combinatorics
- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
5 7
```

**Output**:
```
4
```

### Example 2

**Input**:
```
3
1 1 2
```

**Output**:
```
3
```

### Example 3

**Input**:
```
1
15
```

**Output**:
```
1
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
