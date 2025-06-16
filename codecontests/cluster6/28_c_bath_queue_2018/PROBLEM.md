# 28_C. Bath Queue

**ID:** 28_c_bath_queue_2018
**Difficulty:** 9

## Description

There are n students living in the campus. Every morning all students wake up at the same time and go to wash. There are m rooms with wash basins. The i-th of these rooms contains ai wash basins. Every student independently select one the rooms with equal probability and goes to it. After all students selected their rooms, students in each room divide into queues by the number of wash basins so that the size of the largest queue is the least possible. Calculate the expected value of the size of the largest queue among all rooms.

Input

The first line contains two positive integers n and m (1 ≤ n, m ≤ 50) — the amount of students and the amount of rooms. The second line contains m integers a1, a2, ... , am (1 ≤ ai ≤ 50). ai means the amount of wash basins in the i-th room.

Output

Output single number: the expected value of the size of the largest queue. Your answer must have an absolute or relative error less than 10 - 9.

Examples

Input

1 1
2


Output

1.00000000000000000000


Input

2 2
1 1


Output

1.50000000000000000000


Input

2 3
1 1 1


Output

1.33333333333333350000


Input

7 5
1 1 2 3 1


Output

2.50216960000000070000

## Categories

- combinatorics
- dp
- probabilities

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 2
1 1
```

**Output**:
```
1.500000000000000
```

### Example 2

**Input**:
```
2 3
1 1 1
```

**Output**:
```
1.333333333333333
```

### Example 3

**Input**:
```
7 5
1 1 2 3 1
```

**Output**:
```
2.502169600000002
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
