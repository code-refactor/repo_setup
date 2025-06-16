# 964_C. Alternating Sum

**ID:** 964_c_alternating_sum_12457
**Difficulty:** 9

## Description

You are given two integers a and b. Moreover, you are given a sequence s_0, s_1, ..., s_{n}. All values in s are integers 1 or -1. It's known that sequence is k-periodic and k divides n+1. In other words, for each k ≤ i ≤ n it's satisfied that s_{i} = s_{i - k}.

Find out the non-negative remainder of division of ∑ _{i=0}^{n} s_{i} a^{n - i} b^{i} by 10^{9} + 9.

Note that the modulo is unusual!

Input

The first line contains four integers n, a, b and k (1 ≤ n ≤ 10^{9}, 1 ≤ a, b ≤ 10^{9}, 1 ≤ k ≤ 10^{5}).

The second line contains a sequence of length k consisting of characters '+' and '-'. 

If the i-th character (0-indexed) is '+', then s_{i} = 1, otherwise s_{i} = -1.

Note that only the first k members of the sequence are given, the rest can be obtained using the periodicity property.

Output

Output a single integer — value of given expression modulo 10^{9} + 9.

Examples

Input

2 2 3 3
+-+


Output

7


Input

4 1 5 1
-


Output

999999228

Note

In the first example:

(∑ _{i=0}^{n} s_{i} a^{n - i} b^{i}) = 2^{2} 3^{0} - 2^{1} 3^{1} + 2^{0} 3^{2} = 7

In the second example:

(∑ _{i=0}^{n} s_{i} a^{n - i} b^{i}) = -1^{4} 5^{0} - 1^{3} 5^{1} - 1^{2} 5^{2} - 1^{1} 5^{3} - 1^{0} 5^{4} = -781 ≡ 999999228 \pmod{10^{9} + 9}.

## Categories

- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 2 3 3
+-+
```

**Output**:
```
7
```

### Example 2

**Input**:
```
4 1 5 1
-
```

**Output**:
```
999999228
```

### Example 3

**Input**:
```
743329 973758 92942 82
++----+-++++----+--+++---+--++++-+-+---+++++--+--+++++++--++-+++----+--+++++-+--+-
```

**Output**:
```
299311566
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
