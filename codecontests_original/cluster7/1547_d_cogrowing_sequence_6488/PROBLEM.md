# 1547_D. Co-growing Sequence

**ID:** 1547_d_cogrowing_sequence_6488
**Difficulty:** 10

## Description

A sequence of non-negative integers a_1, a_2, ..., a_n is called growing if for all i from 1 to n - 1 all ones (of binary representation) in a_i are in the places of ones (of binary representation) in a_{i + 1} (in other words, a_i \:\&\: a_{i + 1} = a_i, where \& denotes [bitwise AND](http://tiny.cc/xpy9uz)). If n = 1 then the sequence is considered growing as well.

For example, the following four sequences are growing: 

  * [2, 3, 15, 175] — in binary it's [10_2, 11_2, 1111_2, 10101111_2]; 
  * [5] — in binary it's [101_2]; 
  * [1, 3, 7, 15] — in binary it's [1_2, 11_2, 111_2, 1111_2]; 
  * [0, 0, 0] — in binary it's [0_2, 0_2, 0_2]. 



The following three sequences are non-growing: 

  * [3, 4, 5] — in binary it's [11_2, 100_2, 101_2]; 
  * [5, 4, 3] — in binary it's [101_2, 100_2, 011_2]; 
  * [1, 2, 4, 8] — in binary it's [0001_2, 0010_2, 0100_2, 1000_2]. 



Consider two sequences of non-negative integers x_1, x_2, ..., x_n and y_1, y_2, ..., y_n. Let's call this pair of sequences co-growing if the sequence x_1 ⊕ y_1, x_2 ⊕ y_2, ..., x_n ⊕ y_n is growing where ⊕ denotes [bitwise XOR](http://tiny.cc/bry9uz).

You are given a sequence of integers x_1, x_2, ..., x_n. Find the lexicographically minimal sequence y_1, y_2, ..., y_n such that sequences x_i and y_i are co-growing.

The sequence a_1, a_2, ..., a_n is lexicographically smaller than the sequence b_1, b_2, ..., b_n if there exists 1 ≤ k ≤ n such that a_i = b_i for any 1 ≤ i < k but a_k < b_k.

Input

The first line contains an integer t (1 ≤ t ≤ 10^4). Then t test cases follow.

The first line of each test case contains an integer n (1 ≤ n ≤ 2 ⋅ 10^5) — length of the sequence x_i.

The second line contains n integers x_1, x_2, ..., x_n (0 ≤ x_i < 2^{30}) — elements of the sequence x_i.

It is guaranteed that the sum of n overall all test cases doesn't exceed 2 ⋅ 10^5.

Output

For each test case, print n integers y_1, y_2, ..., y_n (0 ≤ y_i < 2^{30}) — lexicographically minimal sequence such that such that it's co-growing with given sequence x_i.

Example

Input


5
4
1 3 7 15
4
1 2 4 8
5
1 2 3 4 5
4
11 13 15 1
1
0


Output


0 0 0 0 
0 1 3 7 
0 1 0 3 2 
0 2 0 14 
0 

## Categories

- bitmasks
- constructive algorithms
- greedy

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
4
1 3 7 15
4
1 2 4 8
5
1 2 3 4 5
4
11 13 15 1
1
0
```

**Output**:
```
0 0 0 0
0 1 3 7
0 1 0 3 2
0 2 0 14
0
```

### Example 2

**Input**:
```
5
4
1 3 7 15
4
1 2 4 5
5
1 2 3 4 5
4
11 13 15 1
1
0
```

**Output**:
```
0 0 0 0
0 1 3 2
0 1 0 3 2
0 2 0 14
0
```

### Example 3

**Input**:
```
5
4
1 3 7 15
4
1 2 4 5
5
1 2 0 4 5
4
11 13 15 1
1
0
```

**Output**:
```
0 0 0 0
0 1 3 2
0 1 3 3 2
0 2 0 14
0
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
