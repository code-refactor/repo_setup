# 208_C. Police Station

**ID:** 208_c_police_station_7323
**Difficulty:** 9

## Description

The Berland road network consists of n cities and of m bidirectional roads. The cities are numbered from 1 to n, where the main capital city has number n, and the culture capital — number 1. The road network is set up so that it is possible to reach any city from any other one by the roads. Moving on each road in any direction takes the same time.

All residents of Berland are very lazy people, and so when they want to get from city v to city u, they always choose one of the shortest paths (no matter which one).

The Berland government wants to make this country's road network safer. For that, it is going to put a police station in one city. The police station has a rather strange property: when a citizen of Berland is driving along the road with a police station at one end of it, the citizen drives more carefully, so all such roads are considered safe. The roads, both ends of which differ from the city with the police station, are dangerous.

Now the government wonders where to put the police station so that the average number of safe roads for all the shortest paths from the cultural capital to the main capital would take the maximum value.

Input

The first input line contains two integers n and m (2 ≤ n ≤ 100, <image>) — the number of cities and the number of roads in Berland, correspondingly. Next m lines contain pairs of integers vi, ui (1 ≤ vi, ui ≤ n, vi ≠ ui) — the numbers of cities that are connected by the i-th road. The numbers on a line are separated by a space. 

It is guaranteed that each pair of cities is connected with no more than one road and that it is possible to get from any city to any other one along Berland roads.

Output

Print the maximum possible value of the average number of safe roads among all shortest paths from the culture capital to the main one. The answer will be considered valid if its absolute or relative inaccuracy does not exceed 10 - 6.

Examples

Input

4 4
1 2
2 4
1 3
3 4


Output

1.000000000000


Input

11 14
1 2
1 3
2 4
3 4
4 5
4 6
5 11
6 11
1 8
8 9
9 7
11 7
1 10
10 4


Output

1.714285714286

Note

In the first sample you can put a police station in one of the capitals, then each path will have exactly one safe road. If we place the station not in the capital, then the average number of safe roads will also make <image>.

In the second sample we can obtain the maximum sought value if we put the station in city 4, then 6 paths will have 2 safe roads each, and one path will have 0 safe roads, so the answer will equal <image>.

## Categories

- dp
- graphs
- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
11 14
1 2
1 3
2 4
3 4
4 5
4 6
5 11
6 11
1 8
8 9
9 7
11 7
1 10
10 4
```

**Output**:
```
1.714285714
```

### Example 2

**Input**:
```
4 4
1 2
2 4
1 3
3 4
```

**Output**:
```
1.000000000
```

### Example 3

**Input**:
```
34 53
9 6
25 28
27 24
15 18
34 33
27 30
1 4
4 7
11 9
11 8
30 26
15 12
26 23
17 15
29 26
11 15
7 10
14 12
5 9
8 5
2 1
24 21
3 5
14 17
23 20
25 22
32 29
8 6
3 6
33 31
5 2
21 18
16 19
19 22
17 21
14 11
23 27
3 1
34 32
32 30
26 24
17 20
18 20
24 20
2 6
10 13
27 29
14 18
28 31
16 13
9 12
23 21
12 8
```

**Output**:
```
1.998048780
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
