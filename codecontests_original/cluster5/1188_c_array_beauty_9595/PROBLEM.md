# 1188_C. Array Beauty

**ID:** 1188_c_array_beauty_9595
**Difficulty:** 9

## Description

Let's call beauty of an array b_1, b_2, …, b_n (n > 1) — min_{1 ≤ i < j ≤ n} |b_i - b_j|.

You're given an array a_1, a_2, … a_n and a number k. Calculate the sum of beauty over all subsequences of the array of length exactly k. As this number can be very large, output it modulo 998244353.

A sequence a is a subsequence of an array b if a can be obtained from b by deletion of several (possibly, zero or all) elements.

Input

The first line contains integers n, k (2 ≤ k ≤ n ≤ 1000).

The second line contains n integers a_1, a_2, …, a_n (0 ≤ a_i ≤ 10^5).

Output

Output one integer — the sum of beauty over all subsequences of the array of length exactly k. As this number can be very large, output it modulo 998244353.

Examples

Input


4 3
1 7 3 5


Output


8

Input


5 5
1 10 100 1000 10000


Output


9

Note

In the first example, there are 4 subsequences of length 3 — [1, 7, 3], [1, 3, 5], [7, 3, 5], [1, 7, 5], each of which has beauty 2, so answer is 8.

In the second example, there is only one subsequence of length 5 — the whole array, which has the beauty equal to |10-1| = 9.

## Categories

- dp

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 5
1 10 100 1000 10000
```

**Output**:
```
9
```

### Example 2

**Input**:
```
4 3
1 7 3 5
```

**Output**:
```
8
```

### Example 3

**Input**:
```
10 3
10000 20000 30000 40000 50000 60000 70000 80000 90000 100000
```

**Output**:
```
2000000
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
