# 118_D. Caesar's Legions

**ID:** 118_d_caesars_legions_2724
**Difficulty:** 10

## Description

Gaius Julius Caesar, a famous general, loved to line up his soldiers. Overall the army had n1 footmen and n2 horsemen. Caesar thought that an arrangement is not beautiful if somewhere in the line there are strictly more that k1 footmen standing successively one after another, or there are strictly more than k2 horsemen standing successively one after another. Find the number of beautiful arrangements of the soldiers. 

Note that all n1 + n2 warriors should be present at each arrangement. All footmen are considered indistinguishable among themselves. Similarly, all horsemen are considered indistinguishable among themselves.

Input

The only line contains four space-separated integers n1, n2, k1, k2 (1 ≤ n1, n2 ≤ 100, 1 ≤ k1, k2 ≤ 10) which represent how many footmen and horsemen there are and the largest acceptable number of footmen and horsemen standing in succession, correspondingly.

Output

Print the number of beautiful arrangements of the army modulo 100000000 (108). That is, print the number of such ways to line up the soldiers, that no more than k1 footmen stand successively, and no more than k2 horsemen stand successively.

Examples

Input

2 1 1 10


Output

1


Input

2 3 1 2


Output

5


Input

2 4 1 1


Output

0

Note

Let's mark a footman as 1, and a horseman as 2.

In the first sample the only beautiful line-up is: 121

In the second sample 5 beautiful line-ups exist: 12122, 12212, 21212, 21221, 22121

## Categories

- dp

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 1 1 10
```

**Output**:
```
1
```

### Example 2

**Input**:
```
2 3 1 2
```

**Output**:
```
5
```

### Example 3

**Input**:
```
2 4 1 1
```

**Output**:
```
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
