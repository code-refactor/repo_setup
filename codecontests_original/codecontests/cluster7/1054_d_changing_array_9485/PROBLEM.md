# 1054_D. Changing Array

**ID:** 1054_d_changing_array_9485
**Difficulty:** 10

## Description

At a break Vanya came to the class and saw an array of n k-bit integers a_1, a_2, …, a_n on the board. An integer x is called a k-bit integer if 0 ≤ x ≤ 2^k - 1. 

Of course, Vanya was not able to resist and started changing the numbers written on the board. To ensure that no one will note anything, Vanya allowed himself to make only one type of changes: choose an index of the array i (1 ≤ i ≤ n) and replace the number a_i with the number \overline{a_i}. We define \overline{x} for a k-bit integer x as the k-bit integer such that all its k bits differ from the corresponding bits of x. 

Vanya does not like the number 0. Therefore, he likes such segments [l, r] (1 ≤ l ≤ r ≤ n) such that a_l ⊕ a_{l+1} ⊕ … ⊕ a_r ≠ 0, where ⊕ denotes the [bitwise XOR operation](https://en.wikipedia.org/wiki/Bitwise_operation#XOR). Determine the maximum number of segments he likes Vanya can get applying zero or more operations described above.

Input

The first line of the input contains two integers n and k (1 ≤ n ≤ 200 000, 1 ≤ k ≤ 30).

The next line contains n integers a_1, a_2, …, a_n (0 ≤ a_i ≤ 2^k - 1), separated by spaces — the array of k-bit integers.

Output

Print one integer — the maximum possible number of segments with XOR not equal to 0 that can be obtained by making several (possibly 0) operations described in the statement.

Examples

Input

3 2
1 3 0


Output

5

Input

6 3
1 4 4 7 3 4


Output

19

Note

In the first example if Vasya does not perform any operations, he gets an array that has 5 segments that Vanya likes. If he performs the operation with i = 2, he gets an array [1, 0, 0], because \overline{3} = 0 when k = 2. This array has 3 segments that Vanya likes. Also, to get an array with 5 segments that Vanya likes, he can perform two operations with i = 3 and with i = 2. He then gets an array [1, 0, 3]. It can be proven that he can't obtain 6 or more segments that he likes.

In the second example, to get 19 segments that Vanya likes, he can perform 4 operations with i = 3, i = 4, i = 5, i = 6 and get an array [1, 4, 3, 0, 4, 3].

## Categories

- greedy
- implementation

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 2
1 3 0
```

**Output**:
```
5
```

### Example 2

**Input**:
```
6 3
1 4 4 7 3 4
```

**Output**:
```
19
```

### Example 3

**Input**:
```
2 1
0 0
```

**Output**:
```
2
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
