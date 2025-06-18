# 1071_C. Triple Flips

**ID:** 1071_c_triple_flips_5739
**Difficulty:** 9

## Description

You are given an array a of length n that consists of zeros and ones.

You can perform the following operation multiple times. The operation consists of two steps: 

  1. Choose three integers 1 ≤ x < y < z ≤ n, that form an arithmetic progression (y - x = z - y). 
  2. Flip the values a_x, a_y, a_z (i.e. change 1 to 0, change 0 to 1). 



Determine if it is possible to make all elements of the array equal to zero. If yes, print the operations that lead the the all-zero state. Your solution should not contain more than (⌊ n/3 ⌋ + 12) operations. Here ⌊ q ⌋ denotes the number q rounded down. We can show that it is possible to make all elements equal to zero in no more than this number of operations whenever it is possible to do so at all.

Input

The first line contains a single integer n (3 ≤ n ≤ 10^5) — the length of the array.

The second line contains n integers a_1, a_2, …, a_n (0 ≤ a_i ≤ 1) — the elements of the array.

Output

Print "YES" (without quotes) if the answer exists, otherwise print "NO" (without quotes). You can print each letter in any case (upper or lower).

If there is an answer, in the second line print an integer m (0 ≤ m ≤ (⌊ n/3 ⌋ + 12)) — the number of operations in your answer.

After that in (i + 2)-th line print the i-th operations — the integers x_i, y_i, z_i. You can print them in arbitrary order.

Examples

Input

5
1 1 0 1 1


Output

YES
2
1 3 5
2 3 4


Input

3
0 1 0


Output

NO

Note

In the first sample the shown output corresponds to the following solution: 

  * 1 1 0 1 1 (initial state); 
  * 0 1 1 1 0 (the flipped positions are the first, the third and the fifth elements); 
  * 0 0 0 0 0 (the flipped positions are the second, the third and the fourth elements). 



Other answers are also possible. In this test the number of operations should not exceed ⌊ 5/3 ⌋ + 12 = 1 + 12 = 13.

In the second sample the only available operation is to flip all the elements. This way it is only possible to obtain the arrays 0 1 0 and 1 0 1, but it is impossible to make all elements equal to zero.

## Categories

- constructive algorithms

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
1 1 0 1 1
```

**Output**:
```
YES
2
3 4 5
1 2 3
```

### Example 2

**Input**:
```
3
0 1 0
```

**Output**:
```
NO
```

### Example 3

**Input**:
```
7
0 0 1 0 0 0 0
```

**Output**:
```
NO
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
