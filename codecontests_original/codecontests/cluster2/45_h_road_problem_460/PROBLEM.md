# 45_H. Road Problem

**ID:** 45_h_road_problem_460
**Difficulty:** 14

## Description

The Berland capital (as you very well know) contains n junctions, some pairs of which are connected by two-way roads. Unfortunately, the number of traffic jams in the capital has increased dramatically, that's why it was decided to build several new roads. Every road should connect two junctions. 

The city administration noticed that in the cities of all the developed countries between any two roads one can drive along at least two paths so that the paths don't share any roads (but they may share the same junction). The administration decided to add the minimal number of roads so that this rules was fulfilled in the Berland capital as well. In the city road network should exist no more than one road between every pair of junctions before or after the reform.

Input

The first input line contains a pair of integers n, m (2 ≤ n ≤ 900, 1 ≤ m ≤ 100000), where n is the number of junctions and m is the number of roads. Each of the following m lines contains a description of a road that is given by the numbers of the connected junctions ai, bi (1 ≤ ai, bi ≤ n, ai ≠ bi). The junctions are numbered from 1 to n. It is possible to reach any junction of the city from any other one moving along roads.

Output

On the first line print t — the number of added roads. Then on t lines print the descriptions of the added roads in the format of the input data. You can use any order of printing the roads themselves as well as the junctions linked by every road. If there are several solutions to that problem, print any of them.

If the capital doesn't need the reform, print the single number 0.

If there's no solution, print the single number -1.

Examples

Input

4 3
1 2
2 3
3 4


Output

1
1 4


Input

4 4
1 2
2 3
2 4
3 4


Output

1
1 3

## Categories

- graphs

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4 4
1 2
2 3
2 4
3 4
```

**Output**:
```
1
1 3
```

### Example 2

**Input**:
```
4 3
1 2
2 3
3 4
```

**Output**:
```
1
1 4
```

### Example 3

**Input**:
```
10 9
7 9
8 9
8 2
10 6
8 3
9 4
2 6
8 5
9 1
```

**Output**:
```
3
7 5
10 4
3 1
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
