# 839_C. Journey

**ID:** 839_c_journey_2458
**Difficulty:** 9

## Description

There are n cities and n - 1 roads in the Seven Kingdoms, each road connects two cities and we can reach any city from any other by the roads.

Theon and Yara Greyjoy are on a horse in the first city, they are starting traveling through the roads. But the weather is foggy, so they can’t see where the horse brings them. When the horse reaches a city (including the first one), it goes to one of the cities connected to the current city. But it is a strange horse, it only goes to cities in which they weren't before. In each such city, the horse goes with equal probabilities and it stops when there are no such cities. 

Let the length of each road be 1. The journey starts in the city 1. What is the expected length (expected value of length) of their journey? You can read about expected (average) value by the link <https://en.wikipedia.org/wiki/Expected_value>.

Input

The first line contains a single integer n (1 ≤ n ≤ 100000) — number of cities.

Then n - 1 lines follow. The i-th line of these lines contains two integers ui and vi (1 ≤ ui, vi ≤ n, ui ≠ vi) — the cities connected by the i-th road.

It is guaranteed that one can reach any city from any other by the roads.

Output

Print a number — the expected length of their journey. The journey starts in the city 1.

Your answer will be considered correct if its absolute or relative error does not exceed 10 - 6.

Namely: let's assume that your answer is a, and the answer of the jury is b. The checker program will consider your answer correct, if <image>.

Examples

Input

4
1 2
1 3
2 4


Output

1.500000000000000


Input

5
1 2
1 3
3 4
2 5


Output

2.000000000000000

Note

In the first sample, their journey may end in cities 3 or 4 with equal probability. The distance to city 3 is 1 and to city 4 is 2, so the expected length is 1.5.

In the second sample, their journey may end in city 4 or 5. The distance to the both cities is 2, so the expected length is 2.

## Categories

- dfs and similar
- dp
- graphs
- probabilities
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
1 2
1 3
3 4
2 5
```

**Output**:
```
2.000000
```

### Example 2

**Input**:
```
4
1 2
1 3
2 4
```

**Output**:
```
1.500000
```

### Example 3

**Input**:
```
1
```

**Output**:
```
0.000000
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
