# 216_B. Forming Teams

**ID:** 216_b_forming_teams_6387
**Difficulty:** 8

## Description

One day n students come to the stadium. They want to play football, and for that they need to split into teams, the teams must have an equal number of people.

We know that this group of people has archenemies. Each student has at most two archenemies. Besides, if student A is an archenemy to student B, then student B is an archenemy to student A.

The students want to split so as no two archenemies were in one team. If splitting in the required manner is impossible, some students will have to sit on the bench.

Determine the minimum number of students you will have to send to the bench in order to form the two teams in the described manner and begin the game at last.

Input

The first line contains two integers n and m (2 ≤ n ≤ 100, 1 ≤ m ≤ 100) — the number of students and the number of pairs of archenemies correspondingly.

Next m lines describe enmity between students. Each enmity is described as two numbers ai and bi (1 ≤ ai, bi ≤ n, ai ≠ bi) — the indexes of the students who are enemies to each other. Each enmity occurs in the list exactly once. It is guaranteed that each student has no more than two archenemies.

You can consider the students indexed in some manner with distinct integers from 1 to n.

Output

Print a single integer — the minimum number of students you will have to send to the bench in order to start the game.

Examples

Input

5 4
1 2
2 4
5 3
1 4


Output

1

Input

6 2
1 4
3 4


Output

0

Input

6 6
1 2
2 3
3 1
4 5
5 6
6 4


Output

2

## Categories

- dfs and similar
- implementation

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6 2
1 4
3 4
```

**Output**:
```
0
```

### Example 2

**Input**:
```
5 4
1 2
2 4
5 3
1 4
```

**Output**:
```
1
```

### Example 3

**Input**:
```
6 6
1 2
2 3
3 1
4 5
5 6
6 4
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
