# 1416_C. XOR Inverse

**ID:** 1416_c_xor_inverse_4402
**Difficulty:** 9

## Description

You are given an array a consisting of n non-negative integers. You have to choose a non-negative integer x and form a new array b of size n according to the following rule: for all i from 1 to n, b_i = a_i ⊕ x (⊕ denotes the operation [bitwise XOR](https://en.wikipedia.org/wiki/Bitwise_operation#XOR)).

An inversion in the b array is a pair of integers i and j such that 1 ≤ i < j ≤ n and b_i > b_j.

You should choose x in such a way that the number of inversions in b is minimized. If there are several options for x — output the smallest one.

Input

First line contains a single integer n (1 ≤ n ≤ 3 ⋅ 10^5) — the number of elements in a.

Second line contains n space-separated integers a_1, a_2, ..., a_n (0 ≤ a_i ≤ 10^9), where a_i is the i-th element of a.

Output

Output two integers: the minimum possible number of inversions in b, and the minimum possible value of x, which achieves those number of inversions.

Examples

Input


4
0 1 3 2


Output


1 0


Input


9
10 7 9 10 7 5 5 3 5


Output


4 14


Input


3
8 10 3


Output


0 8

Note

In the first sample it is optimal to leave the array as it is by choosing x = 0.

In the second sample the selection of x = 14 results in b: [4, 9, 7, 4, 9, 11, 11, 13, 11]. It has 4 inversions:

  * i = 2, j = 3; 
  * i = 2, j = 4; 
  * i = 3, j = 4; 
  * i = 8, j = 9. 



In the third sample the selection of x = 8 results in b: [0, 2, 11]. It has no inversions.

## Categories

- bitmasks
- data structures
- divide and conquer
- dp
- greedy
- math
- sortings
- strings
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
8 10 3
```

**Output**:
```
0 8
```

### Example 2

**Input**:
```
9
10 7 9 10 7 5 5 3 5
```

**Output**:
```
4 14
```

### Example 3

**Input**:
```
4
0 1 3 2
```

**Output**:
```
1 0
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
