# 108_D. Basketball Team

**ID:** 108_d_basketball_team_11673
**Difficulty:** 10

## Description

As a German University in Cairo (GUC) student and a basketball player, Herr Wafa was delighted once he heard the news. GUC is finally participating in the Annual Basketball Competition (ABC). 

A team is to be formed of n players, all of which are GUC students. However, the team might have players belonging to different departments. There are m departments in GUC, numbered from 1 to m. Herr Wafa's department has number h. For each department i, Herr Wafa knows number si — how many students who play basketball belong to this department.

Herr Wafa was also able to guarantee a spot on the team, using his special powers. But since he hates floating-point numbers, he needs your help at finding the probability that he will have at least one teammate belonging to his department. 

Note that every possible team containing Herr Wafa is equally probable. Consider all the students different from each other.

Input

The first line contains three integers n, m and h (1 ≤ n ≤ 100, 1 ≤ m ≤ 1000, 1 ≤ h ≤ m) — the number of players on the team, the number of departments in GUC and Herr Wafa's department, correspondingly. 

The second line contains a single-space-separated list of m integers si (1 ≤ si ≤ 100), denoting the number of students in the i-th department. Note that sh includes Herr Wafa.

Output

Print the probability that Herr Wafa will have at least one teammate from his department. If there is not enough basketball players in GUC to participate in ABC, print -1. The answer will be accepted if it has absolute or relative error not exceeding 10 - 6.

Examples

Input

3 2 1
2 1


Output

1


Input

3 2 1
1 1


Output

-1


Input

3 2 1
2 2


Output

0.666667

Note

In the first example all 3 players (2 from department 1 and 1 from department 2) must be chosen for the team. Both players from Wafa's departments will be chosen, so he's guaranteed to have a teammate from his department.

In the second example, there are not enough players.

In the third example, there are three possibilities to compose the team containing Herr Wafa. In two of them the other player from Herr Wafa's department is part of the team.

## Categories

- combinatorics
- dp
- math
- probabilities

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 2 1
1 1
```

**Output**:
```
-1
```

### Example 2

**Input**:
```
3 2 1
2 2
```

**Output**:
```
0.6666666667
```

### Example 3

**Input**:
```
3 2 1
2 1
```

**Output**:
```
1
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
