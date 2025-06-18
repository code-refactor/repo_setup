# 1169_B. Pairs

**ID:** 1169_b_pairs_11885
**Difficulty:** 8

## Description

Toad Ivan has m pairs of integers, each integer is between 1 and n, inclusive. The pairs are (a_1, b_1), (a_2, b_2), …, (a_m, b_m). 

He asks you to check if there exist two integers x and y (1 ≤ x < y ≤ n) such that in each given pair at least one integer is equal to x or y.

Input

The first line contains two space-separated integers n and m (2 ≤ n ≤ 300 000, 1 ≤ m ≤ 300 000) — the upper bound on the values of integers in the pairs, and the number of given pairs.

The next m lines contain two integers each, the i-th of them contains two space-separated integers a_i and b_i (1 ≤ a_i, b_i ≤ n, a_i ≠ b_i) — the integers in the i-th pair.

Output

Output "YES" if there exist two integers x and y (1 ≤ x < y ≤ n) such that in each given pair at least one integer is equal to x or y. Otherwise, print "NO". You can print each letter in any case (upper or lower).

Examples

Input


4 6
1 2
1 3
1 4
2 3
2 4
3 4


Output


NO


Input


5 4
1 2
2 3
3 4
4 5


Output


YES


Input


300000 5
1 2
1 2
1 2
1 2
1 2


Output


YES

Note

In the first example, you can't choose any x, y because for each such pair you can find a given pair where both numbers are different from chosen integers.

In the second example, you can choose x=2 and y=4.

In the third example, you can choose x=1 and y=2.

## Categories

- graphs
- implementation

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
300000 5
1 2
1 2
1 2
1 2
1 2
```

**Output**:
```
YES
```

### Example 2

**Input**:
```
5 4
1 2
2 3
3 4
4 5
```

**Output**:
```
YES
```

### Example 3

**Input**:
```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
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
