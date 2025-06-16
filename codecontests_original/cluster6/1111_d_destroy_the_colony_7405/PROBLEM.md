# 1111_D. Destroy the Colony

**ID:** 1111_d_destroy_the_colony_7405
**Difficulty:** 10

## Description

There is a colony of villains with several holes aligned in a row, where each hole contains exactly one villain.

Each colony arrangement can be expressed as a string of even length, where the i-th character of the string represents the type of villain in the i-th hole. 

Iron Man can destroy a colony only if the colony arrangement is such that all villains of a certain type either live in the first half of the colony or in the second half of the colony.

His assistant Jarvis has a special power. It can swap villains of any two holes, i.e. swap any two characters in the string; he can do this operation any number of times.

Now Iron Man asks Jarvis q questions. In each question, he gives Jarvis two numbers x and y. Jarvis has to tell Iron Man the number of distinct colony arrangements he can create from the original one using his powers such that all villains having the same type as those originally living in x-th hole or y-th hole live in the same half and the Iron Man can destroy that colony arrangement.

Two colony arrangements are considered to be different if there exists a hole such that different types of villains are present in that hole in the arrangements.

Input

The first line contains a string s (2 ≤ |s| ≤ 10^{5}), representing the initial colony arrangement. String s can have both lowercase and uppercase English letters and its length is even.

The second line contains a single integer q (1 ≤ q ≤ 10^{5}) — the number of questions.

The i-th of the next q lines contains two integers x_i and y_i (1 ≤ x_i, y_i ≤ |s|, x_i ≠ y_i) — the two numbers given to the Jarvis for the i-th question.

Output

For each question output the number of arrangements possible modulo 10^9+7.

Examples

Input


abba
2
1 4
1 2


Output


2
0


Input


AAaa
2
1 2
1 3


Output


2
0


Input


abcd
1
1 3


Output


8

Note

Consider the first example. For the first question, the possible arrangements are "aabb" and "bbaa", and for the second question, index 1 contains 'a' and index 2 contains 'b' and there is no valid arrangement in which all 'a' and 'b' are in the same half.

## Categories

- combinatorics
- dp
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
abcd
1
1 3
```

**Output**:
```
8
```

### Example 2

**Input**:
```
abba
2
1 4
1 2
```

**Output**:
```
2
0
```

### Example 3

**Input**:
```
AAaa
2
1 2
1 3
```

**Output**:
```
2
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
