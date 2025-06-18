# 1151_B. Dima and a Bad XOR

**ID:** 1151_b_dima_and_a_bad_xor_6990
**Difficulty:** 8

## Description

Student Dima from Kremland has a matrix a of size n × m filled with non-negative integers.

He wants to select exactly one integer from each row of the matrix so that the bitwise exclusive OR of the selected integers is strictly greater than zero. Help him!

Formally, he wants to choose an integers sequence c_1, c_2, …, c_n (1 ≤ c_j ≤ m) so that the inequality a_{1, c_1} ⊕ a_{2, c_2} ⊕ … ⊕ a_{n, c_n} > 0 holds, where a_{i, j} is the matrix element from the i-th row and the j-th column.

Here x ⊕ y denotes the [bitwise XOR operation](https://en.wikipedia.org/wiki/Bitwise_operation#XOR) of integers x and y.

Input

The first line contains two integers n and m (1 ≤ n, m ≤ 500) — the number of rows and the number of columns in the matrix a.

Each of the next n lines contains m integers: the j-th integer in the i-th line is the j-th element of the i-th row of the matrix a, i.e. a_{i, j} (0 ≤ a_{i, j} ≤ 1023). 

Output

If there is no way to choose one integer from each row so that their bitwise exclusive OR is strictly greater than zero, print "NIE".

Otherwise print "TAK" in the first line, in the next line print n integers c_1, c_2, … c_n (1 ≤ c_j ≤ m), so that the inequality a_{1, c_1} ⊕ a_{2, c_2} ⊕ … ⊕ a_{n, c_n} > 0 holds. 

If there is more than one possible answer, you may output any.

Examples

Input


3 2
0 0
0 0
0 0


Output


NIE


Input


2 3
7 7 7
7 7 10


Output


TAK
1 3 

Note

In the first example, all the numbers in the matrix are 0, so it is impossible to select one number in each row of the table so that their bitwise exclusive OR is strictly greater than zero.

In the second example, the selected numbers are 7 (the first number in the first line) and 10 (the third number in the second line), 7 ⊕ 10 = 13, 13 is more than 0, so the answer is found.

## Categories

- bitmasks
- brute force
- constructive algorithms
- dp

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 2
0 0
0 0
0 0
```

**Output**:
```
NIE
```

### Example 2

**Input**:
```
2 3
7 7 7
7 7 10
```

**Output**:
```
TAK
1 3
```

### Example 3

**Input**:
```
2 2
2 7
2 2
```

**Output**:
```
TAK
2 1
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
