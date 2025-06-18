# 388_D. Fox and Perfect Sets

**ID:** 388_d_fox_and_perfect_sets_5562
**Difficulty:** 10

## Description

Fox Ciel studies number theory.

She thinks a non-empty set S contains non-negative integers is perfect if and only if for any <image> (a can be equal to b), <image>. Where operation xor means exclusive or operation (http://en.wikipedia.org/wiki/Exclusive_or).

Please calculate the number of perfect sets consisting of integers not greater than k. The answer can be very large, so print it modulo 1000000007 (109 + 7).

Input

The first line contains an integer k (0 ≤ k ≤ 109).

Output

Print a single integer — the number of required sets modulo 1000000007 (109 + 7).

Examples

Input

1


Output

2


Input

2


Output

3


Input

3


Output

5


Input

4


Output

6

Note

In example 1, there are 2 such sets: {0} and {0, 1}. Note that {1} is not a perfect set since 1 xor 1 = 0 and {1} doesn't contain zero.

In example 4, there are 6 such sets: {0}, {0, 1}, {0, 2}, {0, 3}, {0, 4} and {0, 1, 2, 3}.

## Categories

- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
```

**Output**:
```
3
```

### Example 2

**Input**:
```
4
```

**Output**:
```
6
```

### Example 3

**Input**:
```
1
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
