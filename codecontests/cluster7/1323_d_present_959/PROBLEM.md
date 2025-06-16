# 1323_D. Present

**ID:** 1323_d_present_959
**Difficulty:** 10

## Description

Catherine received an array of integers as a gift for March 8. Eventually she grew bored with it, and she started calculated various useless characteristics for it. She succeeded to do it for each one she came up with. But when she came up with another one — xor of all pairwise sums of elements in the array, she realized that she couldn't compute it for a very large array, thus she asked for your help. Can you do it? Formally, you need to compute

$$$ (a_1 + a_2) ⊕ (a_1 + a_3) ⊕ … ⊕ (a_1 + a_n) \\\ ⊕ (a_2 + a_3) ⊕ … ⊕ (a_2 + a_n) \\\ … \\\ ⊕ (a_{n-1} + a_n) \\\ $$$

Here x ⊕ y is a bitwise XOR operation (i.e. x ^ y in many modern programming languages). You can read about it in Wikipedia: <https://en.wikipedia.org/wiki/Exclusive_or#Bitwise_operation>.

Input

The first line contains a single integer n (2 ≤ n ≤ 400 000) — the number of integers in the array.

The second line contains integers a_1, a_2, …, a_n (1 ≤ a_i ≤ 10^7).

Output

Print a single integer — xor of all pairwise sums of integers in the given array.

Examples

Input


2
1 2


Output


3

Input


3
1 2 3


Output


2

Note

In the first sample case there is only one sum 1 + 2 = 3.

In the second sample case there are three sums: 1 + 2 = 3, 1 + 3 = 4, 2 + 3 = 5. In binary they are represented as 011_2 ⊕ 100_2 ⊕ 101_2 = 010_2, thus the answer is 2.

⊕ is the bitwise xor operation. To define x ⊕ y, consider binary representations of integers x and y. We put the i-th bit of the result to be 1 when exactly one of the i-th bits of x and y is 1. Otherwise, the i-th bit of the result is put to be 0. For example, 0101_2   ⊕   0011_2 = 0110_2.

## Categories

- binary search
- bitmasks
- constructive algorithms
- data structures
- math
- sortings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
1 2 3
```

**Output**:
```
2
```

### Example 2

**Input**:
```
2
1 2
```

**Output**:
```
3
```

### Example 3

**Input**:
```
51
50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
```

**Output**:
```
148
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
