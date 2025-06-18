# 762_A. k-th divisor

**ID:** 762_a_kth_divisor_5057
**Difficulty:** very hard

## Description

You are given two integers n and k. Find k-th smallest divisor of n, or report that it doesn't exist.

Divisor of n is any such natural number, that n can be divided by it without remainder.

Input

The first line contains two integers n and k (1 ≤ n ≤ 1015, 1 ≤ k ≤ 109).

Output

If n has less than k divisors, output -1.

Otherwise, output the k-th smallest divisor of n.

Examples

Input

4 2


Output

2


Input

5 3


Output

-1


Input

12 5


Output

6

Note

In the first example, number 4 has three divisors: 1, 2 and 4. The second one is 2.

In the second example, number 5 has only two divisors: 1 and 5. The third divisor doesn't exist, so the answer is -1.

## Categories

- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
12 5
```

**Output**:
```
6
```

### Example 2

**Input**:
```
4 2
```

**Output**:
```
2
```

### Example 3

**Input**:
```
5 3
```

**Output**:
```
-1
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
